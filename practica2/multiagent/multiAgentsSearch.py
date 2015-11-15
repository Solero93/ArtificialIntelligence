# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from game import Directions
from game import Agent
from game import Actions
import util
import time
from copy import copy

class NearestFoodProblem():
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """
    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0 # DO NOT CHANGE
        self.heuristicInfo = {} # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() < self.start[1].count()

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1 # DO NOT CHANGE
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x,y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost

class NearestGhostProblem():
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """
    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), [x.getPosition() for x in startingGameState.getGhostStates()])
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0 # DO NOT CHANGE
        self.heuristicInfo = {} # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return len(state[1]) < len(self.start[1])

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1 # DO NOT CHANGE
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = copy(state[1])
                try:
                    nextFood.remove((nextx,nexty))
                except:
                    pass
                successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x,y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost

class SearchNode():
    """
    Class that represents a Node for uninformed search algorithms
    State -> State that the Node represents
    Action -> the action that made Pacman arrive here
    Parent -> the Node that it came from
    AccumulatedCost -> Cost it took to arrive here
    """
    def __init__(self):
        self._state = None
        self._action = None
        self._parent = None
        self._depth = 0
        self._accumulatedCost = 0
        
    def setState(self, state):
        self._state = state
        return self
    def getState(self):
        return self._state
    
    def setParent(self, parent):
        self._parent = parent
        return self
    def getParent(self):
        return self._parent
    
    def setAction(self, action):
        self._action = action
        return self
    def getAction(self):
        return self._action
    
    def setDepth(self, depth):
        self._depth = depth
        return self
    def getDepth(self):
        return self._depth

    def setAccumulatedCost(self, cost):
        self._accumulatedCost = cost
        return self
    def getAccumulatedCost(self):
        return self._accumulatedCost
    
    # For debugging purposes
    def __str__(self):
        s = "STATE: \n" + str(self._state) + "\n ACTION: " + str(self._action)
        if (self._parent):
            s+="\nPARENT: \n" + str(self._parent.getState()) + "\n"
        else:
            s+="\nPARENT: " + "No parent" + "\n"
        return s

    def __eq__(self, other):
        if isinstance(other, SearchNode):
            return self.getState() == other.getState() and self.getDepth() == other.getDepth()
        return NotImplemented

def manhattanFoodHeuristic(position, problem, info={}):
    return min(map(lambda x : util.manhattanDistance(position[0],x), problem.getStartState()[1].asList() or [(0,0)]))

def manhattanGhostHeuristic(position, problem, info={}):
    return min(map(lambda x : util.manhattanDistance(position[0],x), problem.getStartState()[1] or [(0,0)]))

def aStarSearchWithMaxDepth(problem, heuristic, maxDepth):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    # Closed nodes, initially empty
    astarClosed = []

    # Frontier nodes, initialize with start State
    astarFrontier = util.PriorityQueueWithFunction(
        lambda state:
            state.getAccumulatedCost() + heuristic(state.getState(), problem)
    )
    astarFrontier.push(
        SearchNode()
            .setState(problem.getStartState())
    )

    while True:        
        # If Frontier is Empty -> return failure
        if astarFrontier.isEmpty():
            goalState = None
            break
        
        # Pop Node from Frontier
        currentState = astarFrontier.pop()
        
        # If Node is goal state -> return Node
        if (problem.isGoalState(currentState.getState())):
            goalState = currentState
            break
        
        # If currentState was not already closed, add to closed and explore (add its successors to frontier)
        if currentState not in astarClosed and currentState.getDepth() < maxDepth:
            astarClosed.append(currentState)
            for successor in problem.getSuccessors(currentState.getState()):
                astarFrontier.push(
                    SearchNode()
                        .setState(successor[0])
                        .setAction(successor[1])
                        .setParent(currentState)
                        .setAccumulatedCost(currentState.getAccumulatedCost() + successor[2])
                        .setDepth(currentState.getDepth() + 1)
                )

    # If there's a solution, return actions, otherwise exit
    if goalState:
        return len(getActionsFromGoalState(goalState))
    else:
        return -1

"""
Auxiliar functions
"""
def getActionsFromGoalState(goalState):
    """
    Returns actions to take, given the goal node
    """
    finalActions = []
    currentNode = goalState
    while currentNode.getParent():
        finalActions.insert(0,currentNode.getAction())
        currentNode = currentNode.getParent()
    return finalActions