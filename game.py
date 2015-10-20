from __future__ import division
import pygame
from pygame.locals import *
from gameview import *
from gamemodel import *
from gamecontrol import *


if __name__ == '__main__':
    pygame.init()

    size = (670,610)
    screen = pygame.display.set_mode(size)
    model = GameModel(10, 10)
    view = GameView(model,screen)
    controller = GameController(model)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
#            if event.type == MOUSEMOTION:
#                controller.handle_mouse_event(event)
            # if event.type == KEYDOWN:
                # controller.handle_key_event(event)
        view.draw()
        time.sleep(0.01)

    pygame.quit()
