from __future__ import division
import pygame
import time
from pygame.locals import *

class GameView:
    ''' View class of MVC structure. '''

    def __init__(self, model, screen):
        ''' Init method of of GameView class. Initializes with:

            model: model class of MVC structure
            screen: pygame screen object
            gridwidth: float width of maze in pixels
            posmazestart: top left corner of maze
        '''
        self.model = model
        self.screen = screen
        self.gridwidth=60.0
        self.posmazestart = [60.0,0]

    def draw(self):
        ''' Called to draw all game components each refresh. '''

        # black background
        self.screen.fill(pygame.Color(0,0,0))

        # convert grid locations into pixel coordinates for player and enemy
        (xp,yp)=self.convertpos((self.model.player.x,self.model.player.y))
        (xen,yen)=self.convertpos((self.model.enemy.x,self.model.enemy.y))
        # draw the player
        pygame.draw.circle(self.screen,pygame.Color(0,255,0),(int(xp),int(yp)),int(self.gridwidth*(3/8)),0)

        # draw the enemy
        if self.model.dangerGauge.distance <= 2:
            if self.model.enemy.trapped != 0:
                pygame.draw.circle(self.screen,pygame.Color(215,0,215),(int(xen),int(yen)),int(self.gridwidth*(3/8)),0)
            else:
                pygame.draw.circle(self.screen,pygame.Color(255,0,0),(int(xen),int(yen)),int(self.gridwidth*(3/8)),0)

        # draw map and map elements
        for pos,unit in self.model.mapUnits.iteritems():
            if unit.visible == True:
                self.drawBorders(unit)
            if unit.contains=="key":
                self.drawkey(unit)
            if unit.contains=="trap":
                self.drawtrap(unit)

        self.drawGauge(self.model.dangerGauge)

        pygame.display.update()

    def convertpos(self,pos):
        ''' Converts a grid position into a pixel coordinates.

            pos: integer tuple
        '''
        xp=pos[0]
        yp=pos[1]
        xp1=self.posmazestart[0]+0.5*self.gridwidth+(xp-1)*self.gridwidth
        yp1=self.posmazestart[1]+0.5*self.gridwidth+self.gridwidth*(yp-1)
        return (xp1,yp1)

    def drawGauge(self,dangerGauge):
        ''' Draws the danger gauge based on distance from player to enemy. '''

        pygame.draw.rect(self.screen, pygame.Color(255,255,0), dangerGauge.border, 1)
        pygame.draw.rect(self.screen, pygame.Color(255,0,0), dangerGauge.fill, 0)

    def drawBorders(self,unit):
        ''' Draws the walls of the maze based on wall tuple of each mapUnit. '''

        # define center of a map unit
        x=self.posmazestart[0]+0.5*self.gridwidth+(unit.x-1)*self.gridwidth
        y=self.posmazestart[1]+0.5*self.gridwidth+self.gridwidth*(unit.y-1)

        # define corners of map unit
        nwcorner = [x-0.5*self.gridwidth,y-0.5*self.gridwidth]
        necorner = [x+0.5*self.gridwidth,y-0.5*self.gridwidth]
        swcorner = [x-0.5*self.gridwidth,y+0.5*self.gridwidth]
        secorner = [x+0.5*self.gridwidth,y+0.5*self.gridwidth]

        # list representing different colors of maze elements
        colors=[pygame.Color(255,255,255),pygame.Color(255,0,0),pygame.Color(255,215,0)]

        # draw a wall, door, or exit based on map unit's walls
        if unit.walls[0] in [1,2,3]:
            pygame.draw.line(self.screen, colors[unit.walls[0]-1],nwcorner,necorner)
        if unit.walls[1] in [1,2,3]:
            pygame.draw.line(self.screen,colors[unit.walls[1]-1],necorner,secorner)
        if unit.walls[2] in [1,2,3]:
            pygame.draw.line(self.screen,colors[unit.walls[2]-1],swcorner,secorner)
        if unit.walls[3] in [1,2,3]:
            pygame.draw.line(self.screen,colors[unit.walls[3]-1],nwcorner,swcorner)

    def drawkey(self,unit):
        ''' Draw a blue circle to represent the key. '''

        (x,y)=self.convertpos((unit.x,unit.y))
        pygame.draw.circle(self.screen,pygame.Color(0,0,255),(int(x),int(y)),int(self.gridwidth*(1/8)),0)

    def drawtrap(self,unit):
        ''' Draw a purple circle to represent a trap. '''

        (x,y)=self.convertpos((unit.x,unit.y))
        pygame.draw.circle(self.screen,pygame.Color(215,0,215),(int(x),int(y)),int(self.gridwidth*(1/8)),0)


    def drawIntro(self):
        ''' Draw intro screen with prompt to start game. '''

        self.screen.fill(pygame.Color(0,0,0))
        font = pygame.font.SysFont('Calibri', 30, True, False)
        text = font.render("Press p to start",True,(0, 0, 255))
        self.screen.blit(text, [250, 250])
        pygame.display.update()

    def drawWin(self):
        ''' Draw screen if you win. '''

        self.screen.fill(pygame.Color(0,0,0))
        font = pygame.font.SysFont('Calibri', 30, True, False)
        text = font.render("YOU WON", True, (0, 255, 0))
        self.screen.blit(text, [250, 250])
        pygame.display.update()

    def drawLost(self):
        ''' Draw screen if you lose. '''

        self.screen.fill(pygame.Color(0,0,0))
        font = pygame.font.SysFont('Calibri', 30, True, False)
        text = font.render("YOU LOST", True, (255, 0, 0))
        self.screen.blit(text, [250, 250])
        pygame.display.update()