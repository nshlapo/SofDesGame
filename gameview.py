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
            if unit.contains=="key":
                self.drawcontains(unit)


        (xp,yp)=self.convertpos((self.model.player.x,self.model.player.y))
        (xen,yen)=self.convertpos((self.model.enemy.x,self.model.enemy.y))
        # xp=self.model.player.x
        # yp=self.model.player.y
        # xp1=self.posmazestart[0]+0.5*self.gridwidth+(xp-1)*self.gridwidth
        # yp1=self.posmazestart[1]+0.5*self.gridwidth+self.gridwidth*(yp-1)

        # xen=self.model.enemy.x
        # yen=self.model.enemy.y
        # xen1=self.posmazestart[0]+0.5*self.gridwidth+(xen-1)*self.gridwidth
        # yen1=self.posmazestart[1]+0.5*self.gridwidth+self.gridwidth*(yen-1)



        # draw the player
        pygame.draw.circle(self.screen,pygame.Color(0,255,0),(int(xp),int(yp)),int(self.gridwidth*(3/8)),0)
        # draw the enemy
        pygame.draw.circle(self.screen,pygame.Color(255,0,0),(int(xen),int(yen)),int(self.gridwidth*(3/8)),0)
        # draw the danger gauge
        self.drawGauge(self.model.dangerGauge)
            #draw enemy
            #draw keys
            #draw traps
        pygame.display.update()

    def convertpos(self,pos):
        xp=pos[0]
        yp=pos[1]
        xp1=self.posmazestart[0]+0.5*self.gridwidth+(xp-1)*self.gridwidth
        yp1=self.posmazestart[1]+0.5*self.gridwidth+self.gridwidth*(yp-1)
        return (xp1,yp1)

    def drawGauge(self,dangerGauge):
        pygame.draw.rect(self.screen, pygame.Color(255,255,0), dangerGauge.border, 1)
        pygame.draw.rect(self.screen, pygame.Color(255,0,0), dangerGauge.fill, 0)

    def drawBorders(self,unit):
        x=self.posmazestart[0]+0.5*self.gridwidth+(unit.x-1)*self.gridwidth
        y=self.posmazestart[1]+0.5*self.gridwidth+self.gridwidth*(unit.y-1)
        nwcorner = [x-0.5*self.gridwidth,y-0.5*self.gridwidth]
        necorner = [x+0.5*self.gridwidth,y-0.5*self.gridwidth]
        swcorner = [x-0.5*self.gridwidth,y+0.5*self.gridwidth]
        secorner = [x+0.5*self.gridwidth,y+0.5*self.gridwidth]
        colors=[pygame.Color(255,255,255),pygame.Color(255,0,0),pygame.Color(0,255,0)]
        if unit.walls[0] in [1,2,3]:
            pygame.draw.line(self.screen, colors[unit.walls[0]-1],nwcorner,necorner)
        if unit.walls[1] in [1,2,3]:
            pygame.draw.line(self.screen,colors[unit.walls[1]-1],necorner,secorner)
        if unit.walls[2] in [1,2,3]:
            pygame.draw.line(self.screen,colors[unit.walls[2]-1],swcorner,secorner)
        if unit.walls[3] in [1,2,3]:
            pygame.draw.line(self.screen,colors[unit.walls[3]-1],nwcorner,swcorner)
    def drawcontains(self,unit):
        (x,y)=self.convertpos((unit.x,unit.y))
        pygame.draw.circle(self.screen,pygame.Color(0,0,255),(int(x),int(y)),int(self.gridwidth*(1/8)),0)
