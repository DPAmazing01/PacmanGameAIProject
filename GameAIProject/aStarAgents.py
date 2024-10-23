from game import *
import util
from util import PriorityQueue

class AStarAgent(Agent):
    def __init__(self, evalfunc='foodHeuristic', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalfunc, globals())
        self.depth = int(depth)

    def getAction(self, gameState):
        # Perform A* search to find path to nearest food
        action = self.aStarSearch(gameState, self.evaluationFunction)
        return action

    def aStarSearch(self, gameState, heuristic):
    # Priority queue for A* search
        openList = util.PriorityQueue()
        openList.push((gameState, []), 0)
        visited = set()

        while not openList.isEmpty():
            currentState, actions = openList.pop()
            if currentState in visited:
                continue
            visited.add(currentState)

            # Check if current state has food
            if currentState.getFood().count() < gameState.getFood().count():
                # Found a state with food, return the action to get there
                return actions[0] if actions else Directions.STOP

            for action in currentState.getLegalActions(0):
                if action == Directions.STOP:
                    continue  # Skip the stop action
                successor = currentState.generateSuccessor(0, action)
                if successor not in visited:
                    # Calculate heuristic cost and push to priority queue
                    cost = len(actions) + 1
                    heuristicCost = cost + heuristic(successor)
                    openList.push((successor, actions + [action]), heuristicCost)

        return Directions.STOP


def foodHeuristic(state):
    # Heuristic: Nearest food + Distance from ghost
    newPos = state.getPacmanPosition()
    newFood = state.getFood()
    newGhostStates = state.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    # Calculate distance to nearest food
    foodDistances = [util.manhattanDistance(newPos, food) for food in newFood.asList()]
    nearestFoodDistance = min(foodDistances) if foodDistances else 0

    # Calculate distance from nearest ghost
    ghostPositions = [ghostState.getPosition() for ghostState in newGhostStates if ghostState.scaredTimer == 0]
    ghostDistances = [util.manhattanDistance(newPos, ghost) for ghost in ghostPositions]
    nearestGhostDistance = min(ghostDistances) if ghostDistances else float('inf')
    
    ghostProximityThreshold = 2  # Define how close is too close
    ghostPenalty = 10  # Define a penalty for being close to a ghost

    if nearestGhostDistance < ghostProximityThreshold:
        return nearestFoodDistance + ghostPenalty * (ghostProximityThreshold - nearestGhostDistance)

    return nearestFoodDistance
