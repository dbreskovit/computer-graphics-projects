import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math


def load_texture(image_path):
    try:
        texture_surface = pygame.image.load(image_path)
        texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
        width, height = texture_surface.get_width(), texture_surface.get_height()
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        return texture_id
    except pygame.error as e:
        print(f"Error loading texture '{image_path}': {e}")
        quit()

vertices = (
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
)
edges = (
    (0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7),
    (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7)
)
faces = (
    (0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
    (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6)
)

default_tex_coords = ((0, 0), (1, 0), (1, 1), (0, 1))

pyramid_vertex_1 = 3
pyramid_vertex_2 = 5

face_texture_mapping = []
for face in faces:
    if pyramid_vertex_1 in face:
        corner_vertex = pyramid_vertex_1
    else:
        corner_vertex = pyramid_vertex_2
    try:
        corner_index = face.index(corner_vertex)
    except ValueError:
        continue
    rotated_coords = list(default_tex_coords)
    rotated_coords = rotated_coords[-corner_index:] + rotated_coords[:-corner_index]
    face_texture_mapping.append(rotated_coords)

def textured_cube(texture_id):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glColor4f(1.0, 1.0, 1.0, 0.7)
    glBegin(GL_QUADS)
    for i, face in enumerate(faces):
        coords_for_face = face_texture_mapping[i]
        for j, vertex_index in enumerate(face):
            glTexCoord2fv(coords_for_face[j])
            glVertex3fv(vertices[vertex_index])
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(1.0)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def wireframe_cube(color, line_width):
    glLineWidth(line_width)
    glColor3fv(color)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def main():
    pygame.init()
    display = (600, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    clock = pygame.time.Clock()

    texture_id = load_texture('textura.jpg')

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        pos_z = -math.sin(pygame.time.get_ticks() / 1000) * 5
        rotation_angle = pygame.time.get_ticks() / 15

        glPushMatrix()
        glTranslatef(0, 0, pos_z)
        glRotatef(-rotation_angle * 1.5, 0, 1, 0)
        glScalef(0.5, 0.5, 0.5)
        wireframe_cube(color=(1.0, 1.0, 0.0), line_width=2.0)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 0, pos_z)
        glRotatef(-rotation_angle * 0.6, -1, 0, 1)
        glScalef(1.5, 1.5, 1.5)
        wireframe_cube(color=(0.0, 1.0, 0.5), line_width=4.0)
        glPopMatrix()

        glPushMatrix()
        local_y_pos = math.sin(pygame.time.get_ticks() / 500) * 0.1
        glTranslatef(0, local_y_pos, pos_z)
        glRotatef(rotation_angle, 1, 1, 1)
        textured_cube(texture_id)
        glPopMatrix()

        pygame.display.flip()
        clock.tick(120)

if __name__ == "__main__":
    main()