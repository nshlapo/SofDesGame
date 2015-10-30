from __future__ import division
import pygame
from pygame.locals import *

class GameController:
    ''' Controller class of MVC structure. '''

    def __init__(self,model):
        ''' Init method of GameController class. Initializes with:

            model: model class of MVC structure
            won: (bool) whether player has won the game
            lost: (bool) whether player has lost the game
        '''
        self.model = model
        self.won = False
        self.lost = False

    def handle_key_event(self, event):
        ''' Event handling method, called whenever there is a key input.

            event: pygame object used to determine what key was pressed
        '''

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

            # return true so trap can be immediately drawn
            return True

    def collision_check(self, mapUnits, player, direction):
        ''' Method used to check whether player can move in input direction.

            mapUnits: (dictionary) map units encoding maze information
            player: (Player) current initialized player object
            direction: (int) represents which way the user wants to move
        '''

        currUnit = mapUnits[(player.x, player.y)]

        if currUnit.walls[direction] is 1:
            print "Can't move there"

        else:
            # if there is no wall
            if currUnit.walls[direction] is 0:
                player.updatepos(currUnit, direction)
                mapUnits[player.x, player.y].visible = True

            # if there is a door
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

            # if there is an exit
            if currUnit.walls[direction] is 3:
                self.won = True
                print "You win"

            # update enemy position after moving player
            self.model.enemy.updatepos(self.model)
            self.trapCheck(self.model.enemy, self.model.mapUnits)

            # update danger gauge and check if enemy has reached player
            self.model.dangerGauge.update()
            if self.model.dangerGauge.distance == 0 and not self.model.enemy.trapped:
                self.lost = True

    def trapCheck(self, enemy, mapUnits):
        ''' Check if enemy has moved onto a trap, and freeze them for 2 moves. '''

        ex = enemy.x
        ey = enemy.y

        if mapUnits[ex, ey].contains is "trap":
            enemy.trapped = 2
            mapUnits[ex, ey].contains = ""

    def placeTrap(self, mapUnits, player):
        ''' Check if player has any traps left, if true place one in current unit. '''

        if player.trap > 0:
            currUnit = mapUnits[player.x, player.y]
            currUnit.contains = "trap"
            player.trap -= 1