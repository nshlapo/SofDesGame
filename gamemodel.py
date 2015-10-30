from __future__ import division
import pygame
from random import *
from pygame.locals import *

class GameModel:
    '''
    Model part of the Maze game
    Creates game model including random maze, randomly placed exit, door, and key
    Takes in xsize, ysize which are integers indicating the size of the map. 
    '''
    def __init__(self,xsize,ysize):
        '''MapUnits are dictionary of instances of mapunit that has its position (x,y) tuple as the key
        '''
        self.xsize=xsize
        self.ysize=ysize
        self.mapUnits = {}
        for i in range(xsize):
            for j in range(ysize):
                self.mapUnits[i+1,j+1]=MapUnit((i+1,j+1),"")
        '''random maze generator generates the maze through the following step:
            First, create grid points that walls can get attached to.
            Second, it creates wall on the boundaries.
            Third, it then recursively attaches wall from a grid that has wall to a grid that has no wall attached.

            self.wall is the list of grids that has wall attached to them,
            self.nowall is the list of grids that has no wall attached.
        '''        
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
        '''After making the maze, the exit is created at the boundary that is farthest away from the player.
            self.cangetto_numsteps essentially marks every mapUnit with the number of steps away from the player.
            Then, self.createexit creates an exit at boundary units that has the largest number of steps away.
        '''
        #marks every mapunit with shortest number of steps to get to certain position starting from player
        self.cangetto_numsteps(self.mapUnits[(self.player.x,self.player.y)],1,0)
        exitunit=self.createexit()
        '''self.cangetto_numsteps is called again this time marking how many steps away every mapunit is from the exit.
            By adding the number of steps away from the player with the number of steps away from the exit, we can get the shortest path.
            Basically following the mapUnits with smallest sum of the numsteps will lead you to the exit.
            The shortest path is appended to self.path through function self.findexit.
        '''
        #marks every mapunit with shortest number of steps to get to certain position starting from the exit
        self.cangetto_numsteps(self.mapUnits[(exitunit.x,exitunit.y)],1,1)
        #finds shortest path to exit and appends to self.path
        self.findexit(self.mapUnits[(self.player.x,self.player.y)])
        print "path", self.path
        '''Door is created along the shortest path to the exit. This prevents the player from exiting without getting the key and going through the door.
            beforedoor is list of mapUnits that can be reached by the player before going through the door.
            self.createkey places the key on mapunit that is certain distance away from the player, and also is before door.
        '''
        doorunit = self.createdoor()
        beforedoor=self.beforedoor(doorunit)
        keypos=self.createkey(beforedoor)
        print "keypos",keypos
        '''Any mapunits that the player has been is marked visible.
        '''
        self.mapUnits[self.player.x, self.player.y].visible = True
        '''positioning enemy and initializing the dangerGauge which tells you how far the player is from the enemy'''
        self.enemy = Enemy((5,5), self.player, self.mapUnits)
        self.dangerGauge = DangerGauge(self.player, self.enemy)

    #clears all numstep markers. The algorithm used to get the shortest path to the exit from player is used for enemy to chase the player. 
    #Since it is using the same markers, it is necessary to clear the markers.
    def clearmapmarker(self):
        for i in range(self.xsize):
            for j in range(self.ysize):
                self.mapUnits[(i+1),(j+1)].numsteps=[0,0]

    #ramdom maze generator. marks where the walls should be on the mapunits.
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

    #generates walls between grid1 and grid2 by marking the mapunits that has the grids as the vertices.
    #input = grid1, grid2 that are tuples like:(xpos,ypos)
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

    #prints adjacent grids with wall
    #inputs grid point (xpos,ypos) tuple, and list of grids with wall.
    #outputs list of grids with wall.
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

    
    #recursive function that marks all the units with number of steps(explained in detail in gamemodel)
    #input: current unit of the player or exit, i=0 to mark from player to exit, and i=1 to mark from exit to player
    def cangetto_numsteps(self,currUnit,step,i):
        currUnit.numsteps[i]=step
        cangetto=self.mapunitcangetto(currUnit,i)
        if len(cangetto)!=0:
            for pos in cangetto:
                self.cangetto_numsteps(self.mapUnits[pos],step+1,i)


    #prints adjacent units that player can get to. 
    #input:Takes the current position. i=0 going from player - exit, i=1 when going from exit-player
    #output:list of units you can get to from current position
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

    #finds the shortest path to the exit.
    #input:position of the player
    #returns the shortest path to the exit
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
    #input: current unit
    #output: units you can go that is around you.
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

    #creates door in the essential place in between the player and the exit. 
    #returns the unit that the door is placed.
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

    #takes the unit where the door is placed and returns every mapunit that player can get to without getting through the door.
    #input: doorunit
    #output: list of units before door.
    def beforedoor(self,doorunit):
        beforedoor=[]
        for i in range(self.xsize):
            for j in range(self.ysize):
                if self.mapUnits[i+1,j+1].numsteps[0]<doorunit.numsteps[0] and self.mapUnits[i+1,j+1].numsteps[1]>doorunit.numsteps[1]:
                    beforedoor.append((i+1,j+1))

        return beforedoor

    #creates key farthest away from player in mapunit that player can reach without going through the door.
    #input:takes the list of units before door,
    #output:position of the key.
    def createkey(self,beforedoor):
        keypos=(self.player.x,self.player.y)
        for pos in beforedoor:
            if self.mapUnits[pos].numsteps[0]>self.mapUnits[keypos].numsteps[0]:
                keypos=pos

        self.mapUnits[keypos].contains="key"
        return pos





class Player:
    '''takes in position tuple pos. automatically creates trap and key attributes which refers to possession of the key or trap of the player
        takes in the whole dictionary of mapUnits because it is necessary for the enemy to chase the player.
    '''
    def __init__(self,pos, mapUnits):
        self.x = pos[0]
        self.y = pos[1]
        self.trap = 3
        self.key = False
        self.mapUnits = mapUnits

    #function that updates the position of the player.
    #input: position of the currently placed unit, and the direction input from the game user through gamecontrol
    #gets the key if the unit that player is moving to has key.
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

class Enemy:
    '''takes the tuple pos, instance of the player class, and the whole dictionary of mapunits.
        player and the dictionary of mapunits is necessary to make the enemy chase the player.
        When the enemy gets trapped, self.trapped becomes 2, and enemy is paralyzed for 2 moves.
    '''
    def __init__(self,pos,player, mapUnits):
        self.x = pos[0]
        self.y = pos[1]
        self.visible = False
        self.player = player
        self.mapUnits = mapUnits
        self.trapped = 0

    #Updates the position of the model through the algorithm that finds the shortest path from the enemy to the player.
    #takes the class model to utilize the methods that were defined within the model class that were used to find the shortest path to exit from player.
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


    #looks at the mapunit around the enemy's position and follows the unit that has the lowest sum of the numstep marker.
    #takes in the mapunits dictionary.
    def chaseplayer(self,mapUnits):
        currUnit=self.mapUnits[self.x,self.y]
        cangetto=[]

        for index, wall in enumerate(currUnit.walls):
            if wall == 0:
                cangetto.append(index)

        initstep=sum(currUnit.numsteps)

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
        """ takes tuple pos (x,y) and string contains which refers to whether the mapunit has anything in it.
            Walls list has following structure:
            [n, w, s, e]
            0 = open
            1 = wall
            2 = door
            3 = exit

            numsteps are markers that are utilized for random maze generator as well as enemy's AI chasing down the player.
            all mapunits are invisible at first and as the player travels along the maze, each of the mapunit the player's been to will be marked visible=true.
        """
        self.x = pos[0]
        self.y = pos[1]
        self.walls=[0,0,0,0]
        self.contains = contains
        self.visible = False
        self.numsteps=[0,0]

class DangerGauge:
    def __init__(self, player, enemy):
        '''dangerGauge takes the player instance and the enemy instance and computes the distance
           between the enemy and the player.
        '''
        self.player = player
        self.enemy = enemy
        self.update()
        self.border = pygame.Rect(10, 10, 40, 580)

    #updates the dangergauge. distance is computed using d^2=x^2+y^2.
    def update(self):
        dx = self.player.x - self.enemy.x
        dy = self.player.y - self.enemy.y
        self.distance = (dx**2 + dy**2)**.5
        self.fill = pygame.Rect(11, (11+(58*(self.distance))), 38, (58*(10-self.distance) - 2))


