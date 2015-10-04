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

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

class SearchNode():
    """
    Class that represents a Node for searching algorithms like BFS and DFS.
    Position -> tuple (i,j) indicating the (x,y) coordinates inside the Pacman Matrix
    Action -> the action that made Pacman arrive here
    Parent -> the Node that it came from
    """
    def __init__(self):
        self.position = None
        self.action = None
        self.parent = None
        
    def setPosition(self, position):
        self.position = position
        return self
    def getPosition(self):
        return self.position
    
    def setParent(self, parent):
        self.parent = parent
        return self
    def getParent(self):
        return self.parent
    
    def setAction(self, action):
        self.action = action
        return self
    def getAction(self):
        return self.action
    
    # For debugging purposes
    def __str__(self):
        s = " POSITION: " + str(self.position) + "\n ACTION: " + str(self.action)
        if (self.parent):
            s+="\n PARENT: " + str(self.parent.getPosition()) + "\n"
        else:
            s+="\n PARENT: " + "No parent" + "\n"
        return s

    def __eq__(self, other):
        if isinstance(other, SearchNode):
            return self.getPosition() == other.getPosition()
        return NotImplemented


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    # Closed nodes, initially empty
    dfsClosed = []

    # Frontier nodes, initialize with start State
    dfsFrontier = util.Stack()
    dfsFrontier.push(
        SearchNode()
            .setPosition(problem.getStartState())
    )

    while True:        
        # If Frontier is Empty -> return failure
        if dfsFrontier.isEmpty():
            goalState = None
            break
        
        # Pop Node from Frontier Stack
        currentState = dfsFrontier.pop()
        
        # If Node is goal state -> return Node
        if (problem.isGoalState(currentState.getPosition())):
            goalState = currentState
            break
        
        # If currentState was not already closed, add to closed and explore (add its successors to frontier)
        if currentState not in dfsClosed:
            dfsClosed.append(currentState)
            for successor in problem.getSuccessors(currentState.getPosition()):
                dfsFrontier.push(
                    SearchNode()
                        .setPosition(successor[0])
                        .setAction(successor[1])
                        .setParent(currentState)
                )

    # If there's a solution, return actions, otherwise exit
    if goalState:
        return getActionsFromGoalState(goalState)
    else:
        print "This problem is not solvable"
        exit(0)


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first.
       Exactly the same algorithm as DFS, but using a Queue as Frontier instead of Stack 
    """
    # Closed nodes, initially empty
    bfsClosed = []

    # Frontier nodes, initialize with start State
    bfsFrontier = util.Queue()
    bfsFrontier.push(
        SearchNode()
            .setPosition(problem.getStartState())
    )

    while True:        
        # If Frontier is Empty -> return failure
        if bfsFrontier.isEmpty():
            goalState = None
            break
        
        # Pop Node from Frontier Stack
        currentState = bfsFrontier.pop()
        
        # If Node is goal state -> return Node
        if (problem.isGoalState(currentState.getPosition())):
            goalState = currentState
            break
        
        # If currentState was not already closed, add to closed and explore (add its successors to frontier)
        if currentState not in bfsClosed:
            bfsClosed.append(currentState)
            for successor in problem.getSuccessors(currentState.getPosition()):
                bfsFrontier.push(
                    SearchNode()
                        .setPosition(successor[0])
                        .setAction(successor[1])
                        .setParent(currentState)
                )

    # If there's a solution, return actions, otherwise exit
    if goalState:
        return getActionsFromGoalState(goalState)
    else:
        print "This problem is not solvable"
        exit(0)

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    " TODO *** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    " TODO *** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


"""
Auxiliar functions
"""
def printDataStructNodes(dataStruct):
    """
    Prints all the Data from Queue and Stack Data structures
    For debugging purposes.
    """
    from copy import deepcopy
    tmpDataStruct = deepcopy(dataStruct)
    while not tmpDataStruct.isEmpty():
        print tmpDataStruct.pop()

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