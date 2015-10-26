from __future__ import division
import pygame
from random import *
from pygame.locals import *

class GameModel:
    def __init__(self,xsize,ysize):
        self.floor = 0
        self.xsize=xsize
        self.ysize=ysize
        self.mapUnits = {}
        for i in range(xsize):
            for j in range(ysize):
                self.mapUnits[i+1,j+1]=MapUnit((i+1,j+1),"")
        self.wall=[]
        self.nowall=[]
        self.grid=[]
        for i in range(xsize+1):
            for j in range(ysize+1):
                self.grid.append((i,j))
                self.nowall.append((i,j))
        print self.nowall
        self.createmaze()
        self.mapUnits[10, 10].walls[1] = 3
        self.player = Player((1,1))
        self.mapUnits[self.player.x, self.player.y].visible = True
        self.enemy = Enemy((5,5), self.player, self.mapUnits)
        self.dangerGauge = DangerGauge(self.player, self.enemy)

    def createmaze(self):
        #draw the outline walls
        for i in range(self.xsize):
            self.genwall((0,i),(0,i+1))
            self.genwall((self.ysize,i),(self.ysize,i+1))

        for j in range(self.ysize):
            self.genwall((j,0),(j+1,0))
            self.genwall((j,self.ysize),(j+1,self.ysize))

        #draws the maze
        while len(self.nowall)!=0:
            indexnowall=randint(0,len(self.nowall)-1)
            nowall_grid = self.nowall[indexnowall]
            #from nowall to wall grid
            if self.adjacent(nowall_grid,self.wall)!=False:
                adjwithwall=self.adjacent(nowall_grid,self.wall)
                print "printing adjwithwall", adjwithwall
                adjgrid = adjwithwall[randint(0,len(adjwithwall)-1)]
                print adjgrid
                self.genwall(nowall_grid,adjgrid)

        print "Random Maze Generated"


    def genwall(self,grid1,grid2):
        print "printing grids",grid1,grid2
        if grid1==grid2:
            print "They are identical grids"
        else:
            #remove grids from nowall list and appending them to wall list
            if grid1 in self.nowall:
                self.nowall.remove(grid1)
                self.wall.append(grid1)
            if grid2 in self.nowall:
                self.nowall.remove(grid2)
                self.wall.append(grid2)

            #Update the mapunit.wall to represent the wall
            #boundaries
            if grid1[1]==0 and grid2[1]==0:
                self.mapUnits[max([grid1[0],grid2[0]]),1].walls[0]=1
            elif grid1[1]==self.ysize and grid2[1]==self.ysize:
                self.mapUnits[max([grid1[0],grid2[0]]),self.ysize].walls[2]=1

            elif grid1[0]==0 and grid2[0]==0:
                self.mapUnits[1,max([grid1[1],grid2[1]])].walls[3]=1
            elif grid1[0]==self.xsize and grid2[0]==self.xsize:
                self.mapUnits[self.xsize,max([grid1[1],grid2[1]])].walls[1]=1

            #other random places
            #checks whether the grids are horizontal or vertical to each other
            elif grid1[0]==grid2[0]:
                self.mapUnits[grid1[0]+1,max([grid1[1],grid2[1]])].walls[3]=1
                self.mapUnits[grid1[0],max([grid1[1],grid2[1]])].walls[1]=1

            elif grid1[1]==grid2[1]:
                self.mapUnits[max([grid1[0],grid2[0]]),grid1[1]].walls[2]=1
                self.mapUnits[max([grid1[0],grid2[0]]),grid1[1]+1].walls[0]=1

            else:
                print "The grids are not adjacent"

    #prints adjacent grids with nowall or with wall
    def adjacent(self,grid,list_wall):
        x=grid[0]
        y=grid[1]
        adjacent = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
        print "print adjacent", adjacent
        adjwithnowall=[]
        for item in adjacent:
            if item in list_wall:
                adjwithnowall.append(item)

        if len(adjwithnowall)>0:
            print "adjwithnowall", adjwithnowall
            return adjwithnowall
        else:
            return False



class Player:
    #takes in position tuple pos. automatically creates trap and key attributes which refers to possession of the key or trap of the player
    def __init__(self,pos):
        self.x = pos[0]
        self.y = pos[1]
        self.trap = False
        self.key = False

    def updatepos(self, currUnit, direction):
        #function update the position of the person
        if direction is 0:
            self.y -= 1
            print "moved up"
        elif direction is 1:
            self.x += 1
            print "moved right"
        elif direction is 2:
            self.y += 1
            print "moved down"
        elif direction is 3:
            self.x -= 1
            print "moved left"

        if currUnit.contains=="key":
                self.key=True
        if currUnit.contains=="trap":
                self.trap=True

class Enemy:
    def __init__(self,pos,player, mapUnits):
        self.x = pos[0]
        self.y = pos[1]
        self.visible = False
        self.player = player
        self.mapUnits = mapUnits

    def updatepos(self):
        # xp = self.player.x
        # yp = self.player.y
        currUnit = self.mapUnits[self.x,self.y]
        go = [i for i, num in enumerate(currUnit.walls) if num is 0]
        rand = randint(0, len(go)-1)
        if go[rand] is 0:
            self.y = self.y - 1
        if go[rand] is 1:
            self.x = self.x + 1
        if go[rand] is 2:
            self.y = self.y + 1
        if go[rand] is 3:
            self.x = self.x - 1
        # a_star()

class MapUnit:
    def __init__(self, pos, contains):
        """ Walls list has following structure:
            [n, w, s, e]
            0 = open
            1 = wall
            2 = door
            3 = exit
        """
        self.x = pos[0]
        self.y = pos[1]
        self.walls=[0,0,0,0]
        self.contains = contains
        self.visible = False

class DangerGauge:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.update()
        self.border = pygame.Rect(10, 10, 40, 580)

    def update(self):
        dx = self.player.x - self.enemy.x
        dy = self.player.y - self.enemy.y
        self.distance = (dx**2 + dy**2)**.5
        self.fill = pygame.Rect(11, (11+(58*(self.distance))), 38, (58*(10-self.distance) - 2))


