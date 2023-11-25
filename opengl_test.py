import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()
display = (640, 480)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

glClearColor(0.1, 0.2, 0.3, 1.0)  # Set clear color to something other than black

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT)  # Clear the screen
    pygame.display.flip()  # Update the display
