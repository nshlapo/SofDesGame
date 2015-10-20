from __future__ import division
import pygame
import time
from pygame.locals import *

class GameView:
    def __init__(self, model,screen):
        self.model = model
        self.screen = screen
        self.gridwidth=60.0
        self.posmazestart = [60.0,0]
    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        #draw walls, stairs, doors, exits based on mapUnit's wall tuple
        for pos,unit in self.model.mapUnits.iteritems():
            if unit.visible == True:
                self.drawBorders(unit)

        xp=self.model.player.pos[0]
        yp=self.model.player.pos[1]
        xp1=self.posmazestart[0]+0.5*self.gridwidth+(xp-1)*self.gridwidth
        yp1=self.posmazestart[1]+0.5*self.gridwidth+self.gridwidth*(yp-1)
        # pygame.draw.circle(self.screen,pygame.Color(0,255,0),(xp1,yp1),self.gridwidth)
        pygame.draw.circle(self.screen,pygame.Color(0,255,0),(int(xp1),int(yp1)),int(self.gridwidth*(3/8)),0)
        self.drawGauge(self.model.dangerGauge)
        pygame.display.update()
            #draw your player
            #draw enemy
            #draw keys
            #draw traps
        

    def drawGauge(self,dangerGauge):
        pygame.draw.rect(self.screen, pygame.Color(255,255,0), dangerGauge.border, 1)
        pygame.draw.rect(self.screen, pygame.Color(255,0,0), dangerGauge.fill, 0)

    def drawBorders(self,unit):
        x=self.posmazestart[0]+0.5*self.gridwidth+(unit.pos[0]-1)*self.gridwidth
        y=self.posmazestart[1]+0.5*self.gridwidth+self.gridwidth*(unit.pos[1]-1)
        nwcorner = [x-0.5*self.gridwidth,y-0.5*self.gridwidth]
        necorner = [x+0.5*self.gridwidth,y-0.5*self.gridwidth]
        swcorner = [x-0.5*self.gridwidth,y+0.5*self.gridwidth]
        secorner = [x+0.5*self.gridwidth,y+0.5*self.gridwidth]
        if unit.walls[0]==1:
            pygame.draw.line(self.screen, pygame.Color(255,255,255),nwcorner,necorner)
        if unit.walls[1]==1:
            pygame.draw.line(self.screen,pygame.Color(255,255,255),necorner,secorner)
        if unit.walls[2]==1:
            pygame.draw.line(self.screen,pygame.Color(255,255,255),swcorner,secorner)
        if unit.walls[3]==1:
            pygame.draw.line(self.screen,pygame.Color(255,255,255),nwcorner,swcorner)




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