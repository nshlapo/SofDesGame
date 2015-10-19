import pygame
from pygame.locals import *

class GameView:

    def __init__(self, model,screen):
        self.model = model
        self.screen = screen

    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        #draw walls, stairs, doors, exits based on mapUnit's wall tuple
        for unit in self.model.mapUnits
            if unit.visible = True:
                drawBorders(unit.walls[0])
                drawBorders(unit.walls[1])
                drawBorders(unit.walls[2])
                drawBorders(unit.walls[3])
            #draw your player
            #draw enemy
            #draw keys
            #draw traps

def drawBorders(border):
    # function to decode our border tuple
    pass
    
# class PyGameWindowView:
#     """ A view of brick breaker rendered in a Pygame window """
#     def __init__(self,model,screen):
#         self.model = model
#         self.screen = screen

#     def draw(self):
#         self.screen.fill(pygame.Color(0,0,0))
#         for brick in self.model.bricks:
#             pygame.draw.rect(self.screen, pygame.Color(brick.color[0],brick.color[1],brick.color[2]),pygame.Rect(brick.x,brick.y,brick.width,brick.height))
#         pygame.draw.rect(self.screen, pygame.Color(self.model.paddle.color[0],self.model.paddle.color[1],self.model.paddle.color[2]),pygame.Rect(self.model.paddle.x,self.model.paddle.y,self.model.paddle.width,self.model.paddle.height))
#         pygame.draw.rect(self.screen, pygame.Color(self.model.ball.color[0],self.model.ball.color[1],self.model.ball.color[2]),pygame.Rect(self.model.ball.x,self.model.ball.y,self.model.ball.width,self.model.ball.height))
#         pygame.display.update()