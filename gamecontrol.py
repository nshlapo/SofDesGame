from __future__ import division
import pygame
from pygame.locals import *

class GameController:
    def __init__(self,model):
        self.model = model
        self.won = False
        self.lost = False


# class GameKeyboardController:
#     def __init__(self,model):
#         self.model = model

    def handle_key_event(self, event):
        if event.key == pygame.K_UP:
            self.collision_check(self.model.mapUnits, self.model.player, 0)
        if event.key == pygame.K_RIGHT:
            self.collision_check(self.model.mapUnits, self.model.player, 1)
        if event.key == pygame.K_DOWN:
            self.collision_check(self.model.mapUnits, self.model.player, 2)
        if event.key == pygame.K_LEFT:
            self.collision_check(self.model.mapUnits, self.model.player, 3)
        if event.key == pygame.K_SPACE:
            self.placeTrap(self.model.mapUnits, self.model.player)

    def collision_check(self, mapUnits, player, direction):
        currUnit = mapUnits[(player.x, player.y)]

        if currUnit.walls[direction] is 1:
            print "Can't move there"

        else:
            if currUnit.walls[direction] is 0:
                player.updatepos(currUnit, direction)
                mapUnits[player.x, player.y].visible = True

            if currUnit.walls[direction] is 2:
                if player.key:
                    currUnit.walls[direction] = 0
                    player.updatepos(currUnit, direction)
                    currUnit = mapUnits[(player.x, player.y)]
                    currUnit.walls[(direction-2)%3] = 0
                    mapUnits[player.x, player.y].visible = True
                else:
                    print "Door is locked"
                    return

            if currUnit.walls[direction] is 3:
                self.won = True
                print "You win"

            self.model.enemy.updatepos(self.model)
            self.trapCheck(self.model.enemy, self.model.mapUnits)
            self.model.dangerGauge.update()
            if self.model.dangerGauge.distance == 0:
                self.lost = True

    def trapCheck(self, enemy, mapUnits):
        ex = enemy.x
        ey = enemy.y
        if mapUnits[ex, ey].contains is "trap":
            enemy.trapped = 2
            mapUnits[ex, ey].contains = ""

    def placeTrap(self, mapUnits, player):
        if player.trap == True:
            print player.trap
            currUnit = mapUnits[player.x, player.y]
            print currUnit.contains
            currUnit.contains = "trap"
            print currUnit.contains
            player.trap = False
            print player.trap
            # print "Trap placed"
        else:
            print "You have no traps"
