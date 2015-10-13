import pygame
from pygame.locals import *

# class BrickBreakerModel:
#     """ Encodes the game state """
#     def __init__(self):
#         self.bricks = []
#         for x in range(20,620,150):
#             brick = Brick((0,255,0),20,100,x,120)
#             self.bricks.append(brick)
#         self.paddle = Paddle((255,255,255),20,100,200,450)

# class Brick:
#     """ Encodes the state of a brick in the game """
#     def __init__(self,color,height,width,x,y):
#         self.color = color
#         self.height = height
#         self.width = width
#         self.x = x
#         self.y = y

# class Paddle:
#     """ Encodes the state of the paddle in the game """
#     def __init__(self,color,height,width,x,y):
#         self.color = color
#         self.height = height
#         self.width = width
#         self.x = x
#         self.y = y

# class Ball:
#     """ Encodes the state of the paddle in the game """
#     def __init__(self,color,height,width,x,y):
#         self.color = color
#         self.height = height
#         self.width = width
#         self.x = x
#         self.y = y