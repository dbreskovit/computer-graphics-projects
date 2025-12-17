import pygame
from pygame.locals import *
import math
from OpenGL.GLU import *
from OpenGL.GL import *

pygame.init()
display = (800, 400)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

def grades():
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)

    glVertex2f(-10, 0)
    glVertex2f(10, 0)

    glVertex2f(0, -5)
    glVertex2f(0, 5)

    glVertex2f(-5, -5)
    glVertex2f(-5, 5)

    glVertex2f(5, -5)
    glVertex2f(5, 5)

    glEnd()

def F2():
    glColor3f(1.0, 0.5, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(-9, 4)
    glVertex2f(-6, 4)
    glVertex2f(-6, 1)
    glVertex2f(-9, 1)
    glEnd()

def F3():
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(-4, 1)
    glVertex2f(-1, 1)
    glVertex2f(-2.5, 4)
    glEnd()

def F4():
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_POLYGON)
    glVertex2f(1, 1)
    glVertex2f(4, 1)
    glVertex2f(4, 3)
    glVertex2f(2.5, 4)
    glVertex2f(1, 3)
    glEnd()

def F5():
    glColor3f(1.0, 0.0, 0.0)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBegin(GL_TRIANGLE_STRIP)
    glVertex2f(5.5, 1)
    glVertex2f(7.5, 1)
    glVertex2f(6.5, 3)
    glVertex2f(8.5, 3)
    glVertex2f(7.5, 1)
    glVertex2f(9.5, 1)
    glEnd()
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

def F6():
    glColor3f(0.0, 0.0, 0.0)
    glLineWidth(3.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(-8.9, -1.0)
    glVertex2f(-6.1, -1.0)
    glVertex2f(-6.1, -4.0)
    glVertex2f(-7.5, -2.6)
    glVertex2f(-8.9, -4.0)
    glEnd()
    glLineWidth(1.0)

def F7():
    glColor3f(0.0, 1.0, 1.0)
    glLineWidth(5.0)
    glBegin(GL_LINES)

    glVertex2f(-5, -0)
    glVertex2f(0, -5)

    glVertex2f(0, -0)
    glVertex2f(-5, -5)
    glEnd()

    glLineWidth(1.0)

def F8():
    glColor3f(1.0, 0.0, 1.0)
    glLineWidth(6.0)

    inset = 0.05
    x_min, x_max = 0.0 + inset, 5.0 - inset
    y_min, y_max = -5.0 + inset, 0.0 - inset

    step = (x_max - x_min) / 5.0

    glBegin(GL_LINES)

    for i in range(1,5):
        x = x_min + i * step
        glVertex2f(x, y_min)
        glVertex2f(x, y_max)

    for j in range(1,5):
        y = y_min + j * step
        glVertex2f(x_min, y)
        glVertex2f(x_max, y)
    glEnd()

    glLineWidth(1.0)

def F9():
    circle_points = 50
    glColor3f(1.0, 1.0, 0.0)
    glLineWidth(2)
    glBegin(GL_LINE_LOOP)
    for i in range(circle_points):
        angle = 2 * math.pi * i / circle_points
        x = math.cos(angle)
        y = math.sin(angle)
        glVertex2f(x + 7.5, y - 2.5)
    glEnd()

def F10():
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex2f(5, 0)
    glVertex2f(10, 0)
    glVertex2f(10, -5)
    glVertex2f(5, -5)
    glEnd()

def main():
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glTranslate(0.0, 0.0, -12)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClearColor(1.0, 1.0, 1.0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        grades()
        F2()
        F3()
        F4()
        F5()
        F6()
        F7()
        F8()
        F10()
        F9()

        pygame.display.flip()
        pygame.time.wait(20)

main()