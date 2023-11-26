"""
Copyright Edgers 2023

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import math

ax = ay = az = 0.0
yaw_mode = True


def resize(width, height):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0 * width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def initialize():
    pygame.init()
    display = (480, 360)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("UAV Visualization")
    resize(*display)
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)


def draw_text(position, textString):
    font = pygame.font.Font(None, 64)
    textSurface = font.render(textString, True, (255, 255, 255, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(*position)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)


def draw_cube():
    """Draw a simple cube with different colors for each face."""
    glBegin(GL_QUADS)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, 0.2, -1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(1.0, 0.2, 1.0)

    glColor3f(1.0, 0.5, 0.0)
    glVertex3f(1.0, -0.2, 1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(1.0, -0.2, -1.0)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)

    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, -1.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, 1.0)

    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, -1.0)

    glEnd()


def draw():
    """
    Render the scene, which includes the cube.
    """
    global ax, ay, az, yaw_mode

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Camera transformation (for this example, we just move the camera a bit back)
    glTranslatef(0.0, 0.0, -7.0)

    # Apply rotations based on sensor data
    if yaw_mode:
        glRotatef(az, 0.0, 1.0, 0.0)  # Yaw
    glRotatef(ax, 1.0, 0.0, 0.0)  # Pitch
    glRotatef(-1*ay, 0.0, 0.0, 1.0)  # Roll

    # Draw the cube
    draw_cube()

    pygame.display.flip()


def update_visualization(new_ax, new_ay, new_az):
    global ax, ay, az
    ax, ay, az = new_ax, new_ay, new_az

    # Apply a scaling factor if needed
    # scale_factor = 1 # Adjust as needed based on your sensor data range
    # ax = new_ax * scale_factor
    # ay = new_ay * scale_factor
    # az = new_az * scale_factor

    # Convert radians to degrees
    # ax = math.degrees(new_ax)
    # ay = math.degrees(new_ay)
    # az = math.degrees(new_az)


def check_for_exit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            return True
    return False


def shutdown():
    pygame.quit()


def main():
    initialize()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        draw()


if __name__ == '__main__':
    main()
