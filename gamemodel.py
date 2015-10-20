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
                self.mapUnits[i+1,j+1]=MapUnit(i+1,j+1,"")


        # self.mapUnits[1,1].walls=[1,0,0,1]
        # self.mapUnits[2,1].walls=[1,0,0,0]
        # self.mapUnits[3,1].walls=[1,0,0,0]
        # self.mapUnits[4,1].walls=[1,1,0,0]

        # self.mapUnits[1,2].walls=[0,1,0,1]
        # self.mapUnits[2,2].walls=[0,1,1,1]
        # self.mapUnits[3,2].walls=[1,0,1,1]
        # self.mapUnits[4,2].walls=[0,1,1,0]

        # self.mapUnits[1,3].walls=[0,1,0,1]
        # self.mapUnits[2,3].walls=[1,0,0,1]
        # self.mapUnits[3,3].walls=[1,0,0,0]
        # self.mapUnits[4,3].walls=[1,1,0,0]

        # self.mapUnits[1,4].walls=[0,0,1,1]
        # self.mapUnits[2,4].walls=[0,1,1,0]
        # self.mapUnits[3,4].walls=[1,0,0,1]
        # self.mapUnits[4,4].walls=[0,1,1,0]
        self.wall=[]
        self.nowall=[]
        self.grid=[]
        for i in range(xsize+1):
            for j in range(ysize+1):
                self.grid.append((i,j))
                self.nowall.append((i,j))
        print self.nowall
        self.drawmaze()
        self.player = Player(1,1)
        self.enemy = Enemy(5,5)
        self.dangerGauge = DangerGauge()

    def drawmaze(self):
        #draw the outline walls
        for i in range(self.xsize):
            self.drawwall((0,i),(0,i+1))
            self.drawwall((self.ysize,i),(self.ysize,i+1))

        for j in range(self.ysize):
            self.drawwall((j,0),(j+1,0))
            self.drawwall((j,self.ysize),(j+1,self.ysize))

        #draws the maze
        while len(self.nowall)!=0:
            indexnowall=randint(0,len(self.nowall)-1)
            indexwall=randint(0,len(self.wall)-1)
            nowall_grid = self.nowall[indexnowall]
            wall_grid =self.wall[indexwall]
            #from nowall to wall grid
            if self.adjacent(nowall_grid,self.wall)!=False:
                adjwithwall=self.adjacent(nowall_grid,self.wall)
                print "printing adjwithwall", adjwithwall
                adjgrid = adjwithwall[randint(0,len(adjwithwall)-1)]
                print adjgrid
                self.drawwall(nowall_grid,adjgrid)

            # #from wall to nowall grid
            # if self.adjacent(wall_grid,self.nowall)!=False:
            #     adjwithnowall=self.adjacent(wall_grid,self.nowall)
            #     print "printing adjwithnowall", adjwithnowall
            #     adjgrid = adjwithnowall[randint(0,len(adjwithnowall)-1)]
            #     self.drawwall(nowall_grid,adjgrid)

        print "Random Maze Generated"


    def drawwall(self,grid1,grid2):
        print "printing grids",grid1,grid2
        if grid1==grid2:
            print "They are identical grids"
        else:
            if grid1 in self.nowall:
                self.nowall.remove(grid1)
                self.wall.append(grid1)
            if grid2 in self.nowall:
                self.nowall.remove(grid2)
                self.wall.append(grid2)
            if grid1[1]==0 and grid2[1]==0:
                self.mapUnits[max([grid1[0],grid2[0]]),1].walls[0]=1
            elif grid1[1]==self.ysize and grid2[1]==self.ysize:
                self.mapUnits[max([grid1[0],grid2[0]]),self.ysize].walls[2]=1

            elif grid1[0]==0 and grid2[0]==0:
                self.mapUnits[1,max([grid1[1],grid2[1]])].walls[3]=1
            elif grid1[0]==self.xsize and grid2[0]==self.xsize:
                self.mapUnits[self.xsize,max([grid1[1],grid2[1]])].walls[1]=1

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
    def __init__(self, x, y, contains):
        """ Walls list has following structure:
            [n, w, s, e]
            0 = open
            1 = wall
            2 = door
            3 = exit
        """
        self.x = x
        self.y = y
        #self.borders = borders
        self.walls=[0,0,0,0]
        self.contains = contains
        self.visible = True

class DangerGauge:
    def __init__(self):
        self.distance = 9
        self.border = pygame.Rect(10, 10, 40, 580)
        self.fill = pygame.Rect(11, (10+(58*(10-self.distance))), 38, (58*(self.distance) - 1))

# class BrickBreakerModel:
#     """ Encodes the game state """
#     def __init__(self):
#         self.bricks = []
#         for x in range(20,620,150):
#             brick = Brick((0,255,0),20,100,x,120)
#             self.bricks.append(brick)
#         self.paddle = Paddle((255,255,255),20,100,200,450)


