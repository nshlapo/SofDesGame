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
        self.path=[]
        for i in range(xsize+1):
            for j in range(ysize+1):
                self.grid.append((i,j))
                self.nowall.append((i,j))
        print self.nowall
        self.createmaze()
        self.player = Player((2,5), self.mapUnits)
        #marks every mapunit with shortest number of steps to get to certain position starting from player
        self.cangetto_numsteps(self.mapUnits[(self.player.x,self.player.y)],1,0)
        exitunit=self.createexit()
        #marks every mapunit with shortest number of steps to get to certain position starting from the exit
        self.cangetto_numsteps(self.mapUnits[(exitunit.x,exitunit.y)],1,1)
        #finds shortest path to exit and appends to self.path
        self.findexit(self.mapUnits[(self.player.x,self.player.y)])
        print "path", self.path
        doorunit = self.createdoor()
        beforedoor=self.beforedoor(doorunit)
        keypos=self.createkey(beforedoor)
        print "keypos",keypos
        self.mapUnits[self.player.x, self.player.y].visible = True
        self.enemy = Enemy((5,5), self.player, self.mapUnits)
        self.dangerGauge = DangerGauge(self.player, self.enemy)

    def clearmapmarker(self):
        for i in range(self.xsize):
            for j in range(self.ysize):
                self.mapUnits[(i+1),(j+1)].numsteps=[0,0]
        
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
                adjgrid = adjwithwall[randint(0,len(adjwithwall)-1)]
                print adjgrid
                self.genwall(nowall_grid,adjgrid)

        print "Random Maze Generated"


    def genwall(self,grid1,grid2):
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
        adjwithnowall=[]
        for item in adjacent:
            if item in list_wall:
                adjwithnowall.append(item)

        if len(adjwithnowall)>0:
            return adjwithnowall
        else:
            return False

    #i=0 from player to exit i=1 from exit to player
    def cangetto_numsteps(self,currUnit,step,i):
        currUnit.numsteps[i]=step
        cangetto=self.mapunitcangetto(currUnit,i)
        if len(cangetto)!=0:
            for pos in cangetto:
                self.cangetto_numsteps(self.mapUnits[pos],step+1,i)


    #prints adjacent units that player can get to. Takes the current position. i=0 going from player - exit, i=1 when going from exit-player
    def mapunitcangetto(self,currUnit,i):
        cangetto=[]
        currentpos=(currUnit.x,currUnit.y)
        if currUnit.walls[0]==0:
            if self.mapUnits[currentpos[0],currentpos[1]-1].numsteps[i]==0:
                cangetto.append((currentpos[0],currentpos[1]-1))

        if currUnit.walls[1]==0:
            if self.mapUnits[currentpos[0]+1,currentpos[1]].numsteps[i]==0:
                cangetto.append((currentpos[0]+1,currentpos[1]))

        if currUnit.walls[2]==0:
            if self.mapUnits[currentpos[0],currentpos[1]+1].numsteps[i]==0:
                cangetto.append((currentpos[0],currentpos[1]+1))

        if currUnit.walls[3]==0:
            if self.mapUnits[currentpos[0]-1,currentpos[1]].numsteps[i]==0:
                cangetto.append((currentpos[0]-1,currentpos[1]))

        return cangetto

    #creates exit farthest away from the player along the boundary
    def createexit(self):
        largestmapunit=self.mapUnits[self.player.x,self.player.y]
        for i in range(self.ysize):
            if self.mapUnits[1,i+1].numsteps[0]>largestmapunit.numsteps[0]:
                largestmapunit=self.mapUnits[1,i+1]

            if self.mapUnits[self.xsize,i+1].numsteps[0]>largestmapunit.numsteps[0]:
                largestmapunit=self.mapUnits[self.xsize,i+1]

        for j in range(self.xsize):
            if self.mapUnits[j+1,1].numsteps[0]>largestmapunit.numsteps[0]:
                largestmapunit=self.mapUnits[j+1,1]
            if self.mapUnits[j+1,self.xsize].numsteps[0]>largestmapunit.numsteps[0]:
                largestmapunit=self.mapUnits[j+1,self.xsize]

        if largestmapunit.x==1:
            largestmapunit.walls[3]=3
        elif largestmapunit.x==self.xsize:
            largestmapunit.walls[1]=3
        elif largestmapunit.y==1:
            largestmapunit.walls[0]=3
        elif largestmapunit.y==self.ysize:
            largestmapunit.walls[2]=3

        return largestmapunit


    #takes an empty list path and returns the shortest path to the exit
    def findexit(self,playerpos):
        self.path.append((playerpos.x,playerpos.y))
        print playerpos.numsteps[0],playerpos.numsteps[1]
        num = playerpos.numsteps[0]+playerpos.numsteps[1]
        cango = self.printcango(playerpos)
        for pos in cango:
            if self.mapUnits[pos].numsteps[0]+self.mapUnits[pos].numsteps[1]==num and pos not in self.path:
                self.findexit(self.mapUnits[pos])
        return

    #prints list of possible places adjacent to current position
    def printcango(self,currUnit):
        cango=[]
        go = [i for i, num in enumerate(currUnit.walls) if num is 0]
        if 0 in go:
            cango.append((currUnit.x,currUnit.y-1))
        if 1 in go:
            cango.append((currUnit.x+1,currUnit.y))
        if 2 in go:
            cango.append((currUnit.x,currUnit.y+1))
        if 3 in go:
            cango.append((currUnit.x-1,currUnit.y))
        return cango

    def createdoor(self):
        cancreatedoor=[]
        i = 0
        while len(cancreatedoor)==0:
            midway = len(self.path)//2+i
            midpos = self.path[midway]
            doorunit = self.mapUnits[midpos]

            if doorunit.walls[0]==0:
                if (doorunit.x,doorunit.y-1) in self.path:
                    cancreatedoor.append(0)
            if doorunit.walls[1]==0:
                if (doorunit.x+1,doorunit.y) in self.path:
                    cancreatedoor.append(1)
            if doorunit.walls[2]==0:
                if (doorunit.x,doorunit.y-1) in self.path:
                    cancreatedoor.append(2)
            if doorunit.walls[3]==0:
                if (doorunit.x,doorunit.y-1) in self.path:
                    cancreatedoor.append(3)
            i+=1
        doorunit.walls[cancreatedoor[0]]=2
        return doorunit

    def beforedoor(self,doorunit):
        beforedoor=[]
        for i in range(self.xsize):
            for j in range(self.ysize):
                if self.mapUnits[i+1,j+1].numsteps[0]<doorunit.numsteps[0] and self.mapUnits[i+1,j+1].numsteps[1]>doorunit.numsteps[1]:
                    beforedoor.append((i+1,j+1))

        return beforedoor

    def createkey(self,beforedoor):
        keypos=(self.player.x,self.player.y)
        for pos in beforedoor:
            if self.mapUnits[pos].numsteps[0]>self.mapUnits[keypos].numsteps[0]:
                keypos=pos

        self.mapUnits[keypos].contains="key"
        return pos





class Player:
    #takes in position tuple pos. automatically creates trap and key attributes which refers to possession of the key or trap of the player
    def __init__(self,pos, mapUnits):
        self.x = pos[0]
        self.y = pos[1]
        self.trap = True
        self.key = False
        self.mapUnits = mapUnits


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
                currUnit.contains=""
        # if currUnit.contains=="trap":
        #         self.trap=True
        #         currUnit.contains=""

class Enemy:
    def __init__(self,pos,player, mapUnits):
        self.x = pos[0]
        self.y = pos[1]
        self.visible = False
        self.player = player
        self.mapUnits = mapUnits
        self.trapped = 0

    def updatepos(self,model):
        model.clearmapmarker()
        if self.trapped != 0:
            self.trapped -= 1
            return
        currUnit = self.mapUnits[self.x,self.y]
        # go = [i for i, num in enumerate(currUnit.walls) if num is 0]
        # rand = randint(0, len(go)-1)
        model.cangetto_numsteps(currUnit,1,0)
        model.cangetto_numsteps(self.mapUnits[(self.player.x,self.player.y)],1,1)
        go = self.chaseplayer(self.mapUnits)
        print "go",go
        if go is 0:
            self.y -= 1
        if go is 1:
            self.x += 1
        if go is 2:
            self.y += 1
        if go is 3:
            self.x -= 1



    def chaseplayer(self,mapUnits):
        currUnit=self.mapUnits[self.x,self.y]
        cangetto=[]
        i=0
        for wall in currUnit.walls:
            if wall ==0:
                cangetto.append(i)
            i+=1
        print "cangetto",cangetto

        initstep=sum(currUnit.numsteps)
        print "initstep", initstep
        for item in cangetto:
            if item ==0:
                if sum(self.mapUnits[self.x,self.y-1].numsteps)==initstep:
                    return item
            elif item ==1:
                if sum(self.mapUnits[self.x+1,self.y].numsteps)==initstep:
                    return item
            elif item ==2:
                if sum(self.mapUnits[self.x,self.y+1].numsteps)==initstep:
                    return item
            elif item ==3:
                if sum(self.mapUnits[self.x-1,self.y].numsteps)==initstep:
                    return item
            else:
                print "you are screwed"



    
    



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
        self.visible = True
        self.numsteps=[0,0]

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


