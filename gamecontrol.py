import pygame
from pygame.locals import *

class PyGameMouseController:
    def __init__(self,model):
        self.model = model

    # def handle_mouse_event(self,event):
    #     if event.type == MOUSEMOTION:
    #         self.model.paddle.x = event.pos[0] - self.model.paddle.width/2.0


# class PyGameKeyboardController:
#     def __init__(self,model):
#         self.model = model

#     def handle_key_event(self, event):
#         if event.type != KEYDOWN:
#             return
#         if event.key == pygame.K_LEFT:
#             self.model.paddle.x += -10
#         if event.key == pygame.K_RIGHT:
#             self.model.paddle.x += 10