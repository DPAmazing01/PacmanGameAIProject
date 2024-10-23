# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.

from game import *
import random, util
import numpy as np

class MultiAgentSearchAgent(Agent):
    def __init__(self, evalfunc='betterEvaluationFunction',depth=2):
        self.index=0
        self.evaluationFunction=util.lookup(evalfunc,globals())
        self.depth=int(depth)

class AlphaBetaAgent(MultiAgentSearchAgent):
    def alphabeta(self, agent, depth, gameState, alpha, beta):
        if gameState.isLose()or gameState.isWin()or depth ==self.depth:
            return self.evaluationFunction(gameState)
        if agent==0:
            value=-999999
            for action in noStopGetLegalActions(agent,gameState):
                value =max(value,self.alphabeta(1,depth,gameState.generateSuccessor(agent,action), alpha,beta))
                alpha =max(alpha,value)
                if beta <= alpha:
                    break
            return value
        else:
            nextAgent =agent+1
            if gameState.getNumAgents() ==nextAgent:
                nextAgent=0
            if nextAgent ==0:
                depth+=1
            for action in noStopGetLegalActions(agent,gameState):
                value=999999
                value =min(value,self.alphabeta(nextAgent, depth,gameState.generateSuccessor(agent,action), alpha,beta))
                beta=min(beta,value)
                if beta<=alpha:
                    break
            return value

    def getAction(self, gameState):
        possible =noStopGetLegalActions(0,gameState)
        alpha=-999999
        beta=999999
        actionscore =[self.alphabeta(0,0,gameState.generateSuccessor(0,action), alpha,beta) for action in possible]
        maxaction= max(actionscore)
        maxindices = [index for index in range(len(actionscore))if actionscore[index]==maxaction]
        chosen =random.choice(maxindices)
        return possible[chosen]

def scoreEvaluation(currentState):
    return currentState.getScore()

def evaluationFunction(currentState, action):
    successor = currentState.generatePacmanSuccessor(action)
    newPos =successor.getPacmanPosition()
    newFood = successor.getFood()
    newGhostStates =successor.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    newFoodList=np.array(newFood.asList())
    distanceToFood =[util.manhattanDistance(newPos, food)for food in newFoodList]
    min =0
    if len(newFoodList)>0:
        min =distanceToFood[np.argmin(distanceToFood)]

    ghostPositions =np.array(successor.getGhostPositions())
    distanceToGhost =[util.manhattanDistance(newPos, ghost)for ghost in ghostPositions]
    min =0
    nearestGhostScaredTime =0
    if len(ghostPositions)>0:
        min = distanceToGhost[np.argmin(distanceToGhost)]
        nearestGhostScaredTime = newScaredTimes[np.argmin(distanceToGhost)]
        if min<=1 and nearestGhostScaredTime ==0:
            return -999999
        if min <=1 and nearestGhostScaredTime >0:
            return 999999

    value = successor.getScore() - min
    if nearestGhostScaredTime > 0:
        value-=min
    else:
        value+=min
    return value

def noStopGetLegalActions(index, state):
    possible = state.getLegalActions(index)
    if Directions.STOP in possible:
        possible.remove(Directions.STOP)
    return possible

def betterEvaluationFunction(currentGameState):
    def _scoreFromGhost(gameState):
        score = 0
        for ghost in gameState.getGhostStates():
            disGhost = manhattanDistance(gameState.getPacmanPosition(), ghost.getPosition())
            if ghost.scaredTimer > 0:
                score += pow(max(8 - disGhost, 0), 2)
            else:
                score -= pow(max(7 - disGhost, 0), 2)
        return score

    def _scoreFromFood(gameState):
        disFood = []
        for food in gameState.getFood().asList():
            disFood.append(1.0 / manhattanDistance(gameState.getPacmanPosition(), food))
        if len(disFood) > 0:
            return max(disFood)
        else:
            return 0

    def _scoreFromCapsules(gameState):
        score = []
        for Cap in gameState.getCapsules():
            score.append(50.0 / manhattanDistance(gameState.getPacmanPosition(), Cap))
        if len(score) > 0:
            return max(score)
        else:
            return 0

    def _suicide(gameState):
        score = 0
        disGhost = 1e6
        for ghost in gameState.getGhostStates():
            disGhost = min(manhattanDistance(gameState.getPacmanPosition(), ghost.getPosition()), disGhost)
        score -= pow(disGhost, 2)
        if gameState.isLose():
            score = 1e6
        return score

    score = currentGameState.getScore()
    scoreGhosts = _scoreFromGhost(currentGameState)
    scoreFood = _scoreFromFood(currentGameState)
    scoreCapsules = _scoreFromCapsules(currentGameState)
    # if score < 800 and currentGameState.getNumFood() <= 1 and len(currentGameState.getCapsules()) == 0:
    #  return _suicide(currentGameState)
    # else:
    return score + scoreGhosts + scoreFood + scoreCapsules

    util.raiseNotDefined()