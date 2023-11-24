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

ax = ay = az = 0.0
yaw_mode = False


def initialize():
    """
    Initialize the visualization module
    :return:
    """
    pygame.init()
    display = (640, 480)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)


def update_visualization(new_ax, new_ay, new_az):
    """
    Update the visualization with new data
    :param new_ax: New ax value
    :param new_ay: New ay value
    :param new_az: New az value
    :return:
    """
    global ax, ay, az
    ax, ay, az = new_ax, new_ay, new_az
    draw()
    pygame.display.flip()


def draw():
    # Clear the screen and depth buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset the view

    # Translate and rotate the model based on sensor data
    # Example translation and rotation (you'll adjust these based on your ax, ay, az values)
    glTranslatef(0.0, 0.0, -5.0)
    glRotatef(ax, 1.0, 0.0, 0.0)  # Rotate by ax degrees around the x-axis
    glRotatef(ay, 0.0, 1.0, 0.0)  # Rotate by ay degrees around the y-axis
    glRotatef(az, 0.0, 0.0, 1.0)  # Rotate by az degrees around the z-axis

    # Begin drawing a cube
    glBegin(GL_QUADS)

    # Front face (z-positive)
    glColor3f(1.0, 0.0, 0.0)  # Red
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)

    # Back face (z-negative)
    glColor3f(0.0, 1.0, 0.0)  # Green
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)

    # Left face (x-negative)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)

    # Right face (x-positive)
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, -1.0)

    # Top face (y-positive)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, -1.0)
    glVertex3f(-1.0, -0.2, -1.0)
    glVertex3f(-1.0, -0.2, 1.0)

    # Bottom face (y-negative)
    glColor3f(1.0, 0.0, 1.0)
    glVertex3f(1.0, 0.2, -1.0)
    glVertex3f(1.0, 0.2, 1.0)
    glVertex3f(1.0, -0.2, 1.0)
    glVertex3f(1.0, -0.2, -1.0)

    glEnd()

    # Flush drawing commands to the graphics card
    glFlush()


def check_for_exit():
    """
    Check for exit event
    :return:
    """
    global yaw_mode
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == KEYDOWN and event.key == K_z:
            yaw_mode = not yaw_mode


def shutdown():
    """
    Clean up and shut down the visualization module
    :return:
    """
    pygame.quit()
