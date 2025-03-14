import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Vertex:
    def __init__(self, x, y, z):
        self.position = np.array([x, y, z], dtype='float32')

class Triangle:
    def __init__(self, vertex1, vertex2, vertex3):
        self.vertices = [vertex1, vertex2, vertex3]

    def draw(self):
        glBegin(GL_TRIANGLES)
        for vertex in self.vertices:
            glVertex3fv(vertex.position)
        glEnd()

class SceneGraph:
    def __init__(self):
        self.triangles = []

    def add_triangle(self, triangle):
        self.triangles.append(triangle)

    def render(self):
        for triangle in self.triangles:
            triangle.draw()

class Camera:
    def __init__(self, position):
        self.position = position
        self.front = np.array([0.0, 0.0, -1.0])
        self.up = np.array([0.0, 1.0, 0.0])

    def move(self, direction):
        self.position += direction

    def get_view_matrix(self):
        target = self.position + self.front
        return gluLookAt(*self.position, *target, *self.up)

class Renderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.camera = Camera(np.array([0.0, 0.0, 5.0]))
        self.scene = SceneGraph()

    def initialize(self):
        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, self.width / self.height, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def render(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.camera.get_view_matrix()
        self.scene.render()
        pygame.display.flip()

def main():
    pygame.init()
    width, height = 800, 600
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

    renderer = Renderer(width, height)
    renderer.initialize()

    # Create a sample triangle
    v1 = Vertex(-1, -1, 0)
    v2 = Vertex(1, -1, 0)
    v3 = Vertex(0, 1, 0)
    triangle = Triangle(v1, v2, v3)
    renderer.scene.add_triangle(triangle)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        renderer.render()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()