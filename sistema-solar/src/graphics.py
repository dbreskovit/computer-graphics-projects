import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

def load_texture(filename):
    try:
        surface = pygame.image.load(filename)
        surface = pygame.transform.flip(surface, False, True)

        if filename.endswith(".png") or surface.get_flags() & SRCALPHA:
            fmt = "RGBA"
            depth = 32
            tex_surface = surface.convert_alpha()
        else:
            fmt = "RGB"
            depth = 24
            tex_surface = surface.convert()

    except Exception as e:
        print(f"Erro textura {filename}: {e}")
        tex_surface = pygame.Surface((64, 64))
        tex_surface.fill((100, 100, 100))
        fmt = "RGB"

    width = tex_surface.get_width()
    height = tex_surface.get_height()
    texture_data = pygame.image.tostring(tex_surface, fmt, 1)

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

    gl_fmt = GL_RGBA if fmt == "RGBA" else GL_RGB
    gluBuild2DMipmaps(GL_TEXTURE_2D, gl_fmt, width, height, gl_fmt, GL_UNSIGNED_BYTE, texture_data)

    return tex_id

def draw_skybox(texture_id):
    glPushMatrix()
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    glColor3f(1, 1, 1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    gluQuadricOrientation(quadric, GLU_INSIDE)
    glRotate(90, 1, 0, 0)
    gluSphere(quadric, 2500, 30, 30)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glPopMatrix()

def draw_orbit(radius):
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glLineWidth(1.0)
    glColor3f(0.15, 0.15, 0.15)
    glBegin(GL_LINE_LOOP)
    segments = 360
    for i in range(segments):
        theta = 2.0 * math.pi * i / segments
        x = radius * math.cos(theta)
        z = radius * math.sin(theta)
        glVertex3f(x, 0, z)
    glEnd()
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)

def draw_body_with_texture(radius, texture_id, emission=False):
    quadric = gluNewQuadric()
    gluQuadricTexture(quadric, GL_TRUE)
    if not emission:
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.1, 0.1, 1.0])
    glBindTexture(GL_TEXTURE_2D, texture_id)
    gluSphere(quadric, radius, 60, 60)

def draw_realistic_ring(inner_radius, outer_radius, texture_id):
    glPushMatrix()
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDisable(GL_CULL_FACE)
    glDisable(GL_LIGHTING)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glColor3f(1, 1, 1)
    glBegin(GL_TRIANGLE_STRIP)
    segments = 180
    for i in range(segments + 1):
        angle = 2.0 * math.pi * i / segments
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        glTexCoord2f(0.0, 0.0);
        glVertex3f(inner_radius * cos_a, inner_radius * sin_a, 0.0)
        glTexCoord2f(1.0, 0.0);
        glVertex3f(outer_radius * cos_a, outer_radius * sin_a, 0.0)
    glEnd()
    glEnable(GL_LIGHTING)
    glEnable(GL_CULL_FACE)
    glDisable(GL_BLEND)
    glPopMatrix()