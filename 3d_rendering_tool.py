import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class Cube:
    def __init__(self, size=1):
        self.size = size
        self.vertices = [
            [size, size, -size],
            [size, -size, -size],
            [-size, -size, -size],
            [-size, size, -size],
            [size, size, size],
            [size, -size, size],
            [-size, -size, size],
            [-size, size, size],
        ]
        self.edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7),
        ]
        self.surfaces = [
            (0, 1, 2, 3),
            (3, 2, 6, 7),
            (7, 6, 5, 4),
            (4, 5, 1, 0),
            (1, 5, 6, 2),
            (4, 0, 3, 7),
        ]

    def draw(self):
        glBegin(GL_QUADS)
        for surface in self.surfaces:
            for vertex in surface:
                glVertex3fv(self.vertices[vertex])
        glEnd()

        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glVertex3fv(self.vertices[vertex])
        glEnd()


def rotate(angle):
    glRotatef(angle, 1, 1, 0)


def setup_view():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (800 / 600), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5)


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    setup_view()

    clock = pygame.time.Clock()
    angle = 0

    cube = Cube(size=1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        rotate(angle)
        cube.draw()

        angle += 1
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()