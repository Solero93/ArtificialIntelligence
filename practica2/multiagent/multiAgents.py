# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
import multiAgentsSearch as ms # Auxiliar class for evaluation function

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()

        nearestGhostDistance = min(map(lambda x : util.manhattanDistance(x.getPosition(),newPos), newGhostStates or [(0,0)]))
        nearestFoodDistance = min(map(lambda x : util.manhattanDistance(x,newPos), newFood or [(0,0)]))
        
        # Taking into account 3 criteria:
        #  - Score
        #  - Manhattan Distance to Nearest Food
        #  - Manhattan Distance to Nearest Ghost 
        #
        # Main idea behind this: 
        #  Pacman needs to get all the food, unless a ghost comes by, in which case it must flee
        
        return successorGameState.getScore() + 5/nearestFoodDistance - (float("inf") if nearestGhostDistance<=1 else 0)

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
      """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
      """

      # Search for the best action.
      #   Default value = -infinity and default action = STOP (in case all evaluation functions would return -infinity)
      maxAction = (float("-infinity"), Directions.STOP)      
      # For each of Pacman's actions, evaluate how good it will be
      #   Return best of them
      for action in gameState.getLegalActions(0):
        miniMaxValue = self.minimaxFunction(gameState=gameState.generateSuccessor(0, action), depth=self.depth, agentIndex=0+1) # start with ghost 1
        maxAction = (miniMaxValue, action) if maxAction[0] < miniMaxValue else maxAction
      return maxAction[1]
        
    def minimaxFunction(self, gameState, depth, agentIndex):
      # If terminal state, return evaluation of state
      if depth == 0 or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
      
      # Assign the next candidates for exploration
      nextAgentIndex = (agentIndex+1) % gameState.getNumAgents() # Rotate between 0 and numAgents
      nextDepth = depth if nextAgentIndex else depth-1           # If the round is over, substract 1 from depth

      # If agent is a ghost (agentIndex!=0)
      #   Minimize each of their actions
      if agentIndex:
        beta = float("infinity")
        for nextAction in gameState.getLegalActions(agentIndex):
          beta = min(beta, self.minimaxFunction(gameState=gameState.generateSuccessor(agentIndex, nextAction), depth=nextDepth, agentIndex=nextAgentIndex))
        return beta
      # If agent is Pacman (agentIndex=0)
      #   Maximize each of its actions          
      else:
        alpha = float("-infinity")
        for nextAction in gameState.getLegalActions(agentIndex):
          alpha = max(alpha, self.minimaxFunction(gameState=gameState.generateSuccessor(agentIndex, nextAction), depth=nextDepth, agentIndex=nextAgentIndex))
        return alpha

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
      """
        Returns the minimax action using self.depth and self.evaluationFunction
      """
      # Here I modified alpha-beta so that it returns the action directly, unlike in MiniMax
      return self.alphabetaFunction(gameState=gameState, depth=self.depth, agentIndex=0, alpha=float("-infinity"), beta=float("infinity"), maxAction=None)

    def alphabetaFunction(self, gameState, depth, agentIndex, alpha, beta, maxAction):
      # If terminal state, return evaluation of state
      if depth == 0 or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
      
      # Assign the next candidates for exploration
      nextAgentIndex = (agentIndex+1) % gameState.getNumAgents() # Rotate between 0 and numAgents
      nextDepth = depth if nextAgentIndex else depth-1           # If the round is over, substract 1 from depth
      
      # If agent is a ghost (agentIndex!=0)
      #   Minimize each of their actions and prune if possible    
      if agentIndex:
        v = float("infinity")
        for nextAction in gameState.getLegalActions(agentIndex):
          v = min(v, self.alphabetaFunction(gameState=gameState.generateSuccessor(agentIndex, nextAction), depth=nextDepth, agentIndex=nextAgentIndex, alpha=alpha, beta=beta, maxAction=maxAction))
          if v < alpha:
            return v
          beta = min(beta, v)
        return v
      # If agent is Pacman (agentIndex=0)
      #   Maximize each of its actions and prune if possible         
      else:
        v = float("-infinity")
        for nextAction in gameState.getLegalActions(agentIndex):
          v = max(v, self.alphabetaFunction(gameState=gameState.generateSuccessor(agentIndex, nextAction), depth=nextDepth, agentIndex=nextAgentIndex, alpha=alpha, beta=beta, maxAction=maxAction))
          if v > beta:
            return v
          # When passing to the next action in the first depth of Pacman's actions
          #   If we improved respect to alpha, we have an action that is better than the previous maxAction
          maxAction = nextAction if depth == self.depth and alpha < v else maxAction 
          alpha = max(alpha, v)
        # If we finished with all the actions Pacman could take in the first depth, we return maxAction
        #   Otherwise, just return v as the algorithm suggests
        return maxAction if depth == self.depth else v
      

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        # Search for the best action.
        #   Default value = -infinity and default action = STOP (in case all evaluation functions would return -infinity)
        maxAction = (float("-infinity"),Directions.STOP)
        # For each of Pacman's actions, evaluate how good it will be
        #   Return best of them
        for action in gameState.getLegalActions(0):
          expectimaxValue = self.expectimaxFunction(gameState=gameState.generateSuccessor(0, action), depth=self.depth, agentIndex=0+1)
          maxAction = (expectimaxValue, action) if maxAction[0] < expectimaxValue else maxAction
        return maxAction[1]
        
    def expectimaxFunction(self, gameState, depth, agentIndex):
      # If terminal state, return evaluation of state
      if depth == 0 or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)
      
      # Assign the next candidates for exploration
      nextAgentIndex = (agentIndex+1) % gameState.getNumAgents()  # Rotate between 0 and numAgents
      nextDepth = depth if nextAgentIndex else depth-1            # If the round is over, substract 1 from depth

      # If agent is a ghost (agentIndex!=0)
      #   Calculate each of their actions' expectations
      if agentIndex:
        beta, numActions = 0, 0
        for nextAction in gameState.getLegalActions(agentIndex):
          numActions += 1
          beta = beta + self.expectimaxFunction(gameState=gameState.generateSuccessor(agentIndex, nextAction), depth=nextDepth, agentIndex=nextAgentIndex)
        return beta/numActions
      # If agent is Pacman (agentIndex=0)
      #   Maximize each of its actions          
      else:
        alpha = float("-infinity")
        for nextAction in gameState.getLegalActions(agentIndex):
          alpha = max(alpha, self.expectimaxFunction(gameState=gameState.generateSuccessor(agentIndex, nextAction), depth=nextDepth, agentIndex=nextAgentIndex))
        return alpha

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION:

      Taking into account 3 criteria:
      - Score
      - Distance to Nearest Food - Using A-star (the main difference between ReflexAgent and betterEvaluationFunction)
      - Manhattan Distance to Nearest Ghost 
    
      Main idea behind this: 
        Pacman needs to get all the food, unless a ghost comes by, in which case it must flee
    """
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood().asList()
    newGhostStates = currentGameState.getGhostStates()
     
    # A-star of limited depth = maxDepth to try to find the distance to the nearest food
      # I've limited the depth, because otherwise it would be very costly
      # Also I saw that I don't really need the information of more depth
    # If A-star cannot find it within this depth
      # Assign the maximum between 
          # maxDepth+1 (minimum real distance to food) and
          # minimum of Manhattan distances to food (an easily calculable measurement of distance)
    maxDepth = 5
    nearestAstarFoodDistance = ms.aStarSearchWithMaxDepth(ms.NearestFoodProblem(currentGameState), ms.manhattanFoodHeuristic, maxDepth)
    nearestManhattanFoodDistance = min(map(lambda x : util.manhattanDistance(x,newPos), newFood or [(0,0)]))
    nearestFoodDistance = nearestAstarFoodDistance if nearestAstarFoodDistance!=-1 else max(maxDepth+1,nearestManhattanFoodDistance)

    # Minimum of Manhattan distance to ghost
    nearestGhostDistance = min(map(lambda x : util.manhattanDistance(x.getPosition(),newPos), newGhostStates or [(0,0)]))

    return 10*currentGameState.getScore() + 100/nearestFoodDistance - (float("inf") if nearestGhostDistance<=1 else 0)

# Abbreviation
better = betterEvaluationFunction