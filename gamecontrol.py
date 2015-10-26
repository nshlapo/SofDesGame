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

    def collision_check(self, mapUnits, player, direction):
        currUnit = mapUnits[(player.x, player.y)]
        if currUnit.walls[direction] is 0:
            player.updatepos(currUnit, direction)
            mapUnits[player.x, player.y].visible = True
            self.model.enemy.updatepos()
            self.model.dangerGauge.update()
            print self.model.dangerGauge.distance
            if self.model.dangerGauge.distance == 0:
                    self.lost = True

        if currUnit.walls[direction] is 2:
            if player.key:
                player.updatepos(currUnit, direction)
                currUnit.walls[direction] = 0
                mapUnits[player.x, player.y].visible = True
                self.model.enemy.updatepos()
                self.model.dangerGauge.update()
                print self.model.dangerGauge.distance
                if self.model.dangerGauge.distance == 0:
                    self.lost = True

        if currUnit.walls[direction] is 3:
            self.won = True
            print "You win"

        else:
            print "Can't move there"