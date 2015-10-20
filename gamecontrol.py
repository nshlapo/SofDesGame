from __future__ import division
import pygame
from pygame.locals import *

class GameController:
    def __init__(self,model):
        self.model = model


class GameKeyboardController:
    def __init__(self,model):
        self.model = model

    def handle_key_event(self, event):
        if event.type != KEYDOWN:
            return
        # if event.key == pygame.K_LEFT:
