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
    pygame.display.set_caption("Maze Wanderer")
    play = True

    while play:
        # initialize MVC elements
        model = GameModel(10, 10)
        view = GameView(model,screen)
        controller = GameController(model)

        # initialize game state bools
        intro  = True
        playing = False
        winning = False
        losing = False

        while intro:
            for event in pygame.event.get():
                if event.type == QUIT:
                    intro = False

                if event.type == KEYDOWN:
                    if event.key == pygame.K_p:
                        intro = False
                        playing = True

            view.drawIntro()
            time.sleep(0.01)

        while playing:
            for event in pygame.event.get():
                if event.type == QUIT:
                    playing = False

                if event.type == KEYDOWN:
                    trap = controller.handle_key_event(event)

                    # update trap if it was placed
                    if trap:
                        view.draw()

                if controller.won == True:
                    playing = False
                    winning = True

                if controller.lost == True:
                    playing = False
                    losing = True

            view.draw()
            time.sleep(0.01)

        while winning:
            for event in pygame.event.get():
                if event.type == QUIT:
                    winning = False

            view.drawWin()
            time.sleep(0.01)

        while losing:
            for event in pygame.event.get():
                if event.type == QUIT:
                    losing = False
                    play = False

                # enable keypress to replay
                if event.type == KEYDOWN:
                    if event.key == pygame.K_p:
                        losing = False

            view.drawLost()
            time.sleep(0.01)

    pygame.quit()