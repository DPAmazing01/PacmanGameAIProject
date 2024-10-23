# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.

from game import *
import random

class KeyboardAgent(Agent):
    WEST_KEY = 'a'
    EAST_KEY = 'a'
    NORTH_KEY = 'a'
    SOUTH_KEY = 'a'
    STOP_KEY = 'a'

    def __init__(self,index=0):
        self.lastMove = Directions.STOP
        self.index = index
        self.keys=[]

    def getAction(self, state):
        from graphicsUtils import keys_waiting
        from graphicsUtils import keys_pressed
        keys= keys_waiting() + keys_pressed()
        if keys!=[]:
            self.keys =keys
        legal = state.getLegalActions(self.index)
        move =self.getMove(legal)

        if move==Directions.STOP:
            if self.lastMove in legal:
                move = self.lastMove

        if (self.STOP_KEY in self.keys) and Directions.STOP in legal:
            move= Directions.STOP
        if move not in legal:
            move =random.choice(legal)

        self.lastMove = move
        return move

    def getMove(self,legal):
        move=Directions.STOP
        if (self.WEST_KEY in self.keys or 'Left' in self.keys) and Directions.WEST in legal:
            move = Directions.WEST
        if (self.EAST_KEY in self.keys or 'Right' in self.keys) and Directions.EAST in legal:
            move = Directions.EAST
        if (self.NORTH_KEY in self.keys or 'Up' in self.keys) and Directions.NORTH in legal:
            move = Directions.NORTH
        if (self.SOUTH_KEY in self.keys or 'Down' in self.keys) and Directions.SOUTH in legal:
            move = Directions.SOUTH
        return move

class KeyboardAgent2(KeyboardAgent):
    WEST_KEY = 'j'
    EAST_KEY = 'l'
    NORTH_KEY = 'i'
    SOUTH_KEY = 'k'
    STOP_KEY = 'u'

    def getMove(self,legal):
        move = Directions.STOP
        if (self.WEST_KEY in self.keys or 'Left' in self.keys) and Directions.WEST in legal:
            move = Directions.WEST
        if (self.EAST_KEY in self.keys or 'Right' in self.keys) and Directions.EAST in legal:
            move = Directions.EAST
        if (self.NORTH_KEY in self.keys or 'Up' in self.keys) and Directions.NORTH in legal:
            move = Directions.NORTH
        if (self.SOUTH_KEY in self.keys or 'Down' in self.keys) and Directions.SOUTH in legal:
            move = Directions.SOUTH
        return move

