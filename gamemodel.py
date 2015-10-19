import pygame
from pygame.locals import *

class GameModel:
    def __init__(self):
        self.floor = 0
        self.mapUnits = []
            for x in
        self.player =



class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.trap = False
        self.key = False


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visible = False

class MapUnit:
    def __init__(self, x, y, borders, key, trap, stair):
        """ Walls tuple has following structure:
            (n, w, s, e)
            0 = open
            1 = wall
            2 = door
            3 = exit
        """
        self.x = x
        self.y = y
        self.borders = borders
        self.key = key
        self.trap = trap
        self.stair = stair
        self.visible = False

# class BrickBreakerModel:
#     """ Encodes the game state """
#     def __init__(self):
#         self.bricks = []
#         for x in range(20,620,150):
#             brick = Brick((0,255,0),20,100,x,120)
#             self.bricks.append(brick)
#         self.paddle = Paddle((255,255,255),20,100,200,450)
