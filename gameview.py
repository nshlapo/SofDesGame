from __future__ import division
import pygame
import time
from pygame.locals import *

class GameView:
    def __init__(self, model, screen):
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

        xp=self.model.player.x
        yp=self.model.player.y
        xp1=self.posmazestart[0]+0.5*self.gridwidth+(xp-1)*self.gridwidth
        yp1=self.posmazestart[1]+0.5*self.gridwidth+self.gridwidth*(yp-1)

        xen=self.model.enemy.x
        yen=self.model.enemy.y
        xen1=self.posmazestart[0]+0.5*self.gridwidth+(xen-1)*self.gridwidth
        yen1=self.posmazestart[1]+0.5*self.gridwidth+self.gridwidth*(yen-1)



        # draw the player
        pygame.draw.circle(self.screen,pygame.Color(0,255,0),(int(xp1),int(yp1)),int(self.gridwidth*(3/8)),0)
        # draw the enemy
        pygame.draw.circle(self.screen,pygame.Color(255,0,0),(int(xen1),int(yen1)),int(self.gridwidth*(3/8)),0)
        # draw the danger gauge
        self.drawGauge(self.model.dangerGauge)
            #draw enemy
            #draw keys
            #draw traps
        pygame.display.update()


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
        if unit.walls[0]==1:
            pygame.draw.line(self.screen, pygame.Color(255,255,255),nwcorner,necorner)
        if unit.walls[1]==1:
            pygame.draw.line(self.screen,pygame.Color(255,255,255),necorner,secorner)
        if unit.walls[2]==1:
            pygame.draw.line(self.screen,pygame.Color(255,255,255),swcorner,secorner)
        if unit.walls[3]==1:
            pygame.draw.line(self.screen,pygame.Color(255,255,255),nwcorner,swcorner)

        if unit.walls[0]==3:
            pygame.draw.line(self.screen, pygame.Color(255,215,0),nwcorner,necorner)
        if unit.walls[1]==3:
            pygame.draw.line(self.screen,pygame.Color(255,215,0),necorner,secorner)
        if unit.walls[2]==3:
            pygame.draw.line(self.screen,pygame.Color(255,215,0),swcorner,secorner)
        if unit.walls[3]==3:
            pygame.draw.line(self.screen,pygame.Color(255,215,0),nwcorner,swcorner)


    def drawIntro(self):
        self.screen.fill(pygame.Color(0,0,0))
        font = pygame.font.SysFont('Calibri', 30, True, False)
        text = font.render("Press p to start",True,(0, 0, 255))
        self.screen.blit(text, [250, 250])
        pygame.display.update()
`
    def drawWin(self):
        self.screen.fill(pygame.Color(0,0,0))
        font = pygame.font.SysFont('Calibri', 30, True, False)
        text = font.render("YOU WON", True, (0, 255, 0))
        self.screen.blit(text, [250, 250])
        pygame.display.update()

    def drawLost(self):
        self.screen.fill(pygame.Color(0,0,0))
        font = pygame.font.SysFont('Calibri', 30, True, False)
        text = font.render("YOU LOST", True, (255, 0, 0))
        self.screen.blit(text, [250, 250])
        pygame.display.update()

