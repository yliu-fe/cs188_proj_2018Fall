# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        # Foods' factor for score
        nearest_food_mandis = 1e9
        foods = newFood.asList()
        for food in foods:
            nearest_food_mandis = min(nearest_food_mandis, manhattanDistance(food,newPos))
        if len(foods) == 0:
            nearest_food_mandis = 0
        
        # Ghosts' factor for score
        nearest_ghost_mandis = 1e9
        for ghost_state in newGhostStates:
            ghost_x, ghost_y = ghost_state.getPosition()
            ghost_x = int(ghost_x)
            ghost_y = int(ghost_y)

            if ghost_state.scaredTimer == 0:
                nearest_ghost_mandis = min(nearest_ghost_mandis, manhattanDistance((ghost_x,ghost_y),newPos))

        return successorGameState.getScore() - 7 / (nearest_ghost_mandis + 1) - nearest_food_mandis/3

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        legal_action = gameState.getLegalActions(0)

        best_action = None
        best_score = -1e9
        for action in legal_action:
            successorState = gameState.generateSuccessor(0, action)
            if self.value(successorState, agentIndex = 1) > best_score:
                best_score = self.value(successorState, agentIndex= 1)
                best_action = action

        return best_action

    def value(self, gameState, depth=0, agentIndex=0):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)

        if agentIndex == 0:
            return self.max_value(gameState, depth)
        else:
            return self.min_value(gameState, depth, agentIndex)
        
    def max_value(self, gameState, depth):
        legal_action = gameState.getLegalActions(0)
        v = -1e9
        for action in legal_action:
            successorState = gameState.generateSuccessor(0, action)
            v = max(v, self.value(successorState, depth, 1))
        return v
    
    def min_value(self, gameState, depth, agentIndex):
        legal_action = gameState.getLegalActions(agentIndex)
        v = 1e9
        for action in legal_action:
            successorState = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == gameState.getNumAgents() - 1:
                v = min(v, self.value(successorState, depth + 1, 0))
            else:
                v = min(v, self.value(successorState, depth, agentIndex + 1))
        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        legal_action = gameState.getLegalActions(0)
        alpha = -1e9
        beta = 1e9
        best_action = None
        best_score = -1e9
        for action in legal_action:
            successorState = gameState.generateSuccessor(0, action)
            successorValue = self.value(successorState, alpha,beta,depth = 0, agentIndex= 1)
            if successorValue > best_score:
                best_score = successorValue
                best_action = action
                alpha = successorValue
        return best_action

    
    def value(self, gameState, alpha, beta, depth = 0, agentIndex = 0):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        
        if agentIndex == 0:
            return self.max_value(gameState, depth, agentIndex, alpha, beta)
        else:
            return self.min_value(gameState, depth, agentIndex, alpha, beta)


    def max_value(self, gameState, depth, agentIndex, alpha, beta):
        legal_action = gameState.getLegalActions(agentIndex)
        value = -1e9
        for action in legal_action:
            successorState = gameState.generateSuccessor(agentIndex, action)
            successorValue = self.value(successorState, alpha, beta, depth, agentIndex+1)
            value = max(successorValue,value)
            if value > beta:
                return value
            alpha = max(value, alpha)
        return value

    def min_value(self, gameState, depth, agentIndex, alpha, beta):
        legal_action = gameState.getLegalActions(agentIndex)
        value = 1e9
        for action in legal_action:
            successorState = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == gameState.getNumAgents() - 1:
                successorValue = self.value(successorState,alpha,beta,depth+1,0)
            else:
                successorValue = self.value(successorState,alpha,beta,depth, agentIndex+1)
            value = min(value,successorValue)
            if value < alpha:
                return value
            beta = min(beta, value)
        return value
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
        "*** YOUR CODE HERE ***"
        legal_action = gameState.getLegalActions(0)
        best_action = None
        best_score = -1e9
        for action in legal_action:
            successorState = gameState.generateSuccessor(0, action)
            successorValue = self.value(successorState, 1, 0)
            if successorValue > best_score:
                best_action = action
                best_score = successorValue
        return best_action
    

    def value(self,gameState,agentIndex, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        
        if agentIndex == 0:
            return self.max_value(gameState,agentIndex,depth)
        else:
            return self.exp_value(gameState,agentIndex,depth)

    def max_value(self, gameState, agentIndex, depth):
        legal_actions = gameState.getLegalActions(agentIndex)
        value = -1e9
        for action in legal_actions:
            successorState = gameState.generateSuccessor(agentIndex,action)
            value = max(value, self.value(successorState,agentIndex+1,depth))
        return value

    def exp_value(self, gameState, agentIndex, depth):
        value = 0
        legal_actions = gameState.getLegalActions(agentIndex)
        for action in legal_actions:
            successorState = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == gameState.getNumAgents() - 1:
                value += self.value(successorState, 0 , depth + 1)
            else:
                value += self.value(successorState, agentIndex + 1, depth)

        return value / len(legal_actions)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"


    # Foods' factor for score
    nearest_food_mandis = 1e9
    foods = currentGameState.getFood().asList()

    if len(foods) == 0:
        nearest_food_mandis = 0
    for food in foods:
        nearest_food_mandis = min(nearest_food_mandis, manhattanDistance(food,currentGameState.getPacmanPosition()))

    # Ghosts' factor for score
    nearest_ghost_mandis = 1e9
    for ghost_state in currentGameState.getGhostStates():
        ghost_x, ghost_y = ghost_state.getPosition()
        ghost_x = int(ghost_x)
        ghost_y = int(ghost_y)

        if ghost_state.scaredTimer == 0:
            nearest_ghost_mandis = min(nearest_ghost_mandis, manhattanDistance((ghost_x,ghost_y),currentGameState.getPacmanPosition()))
    
    return currentGameState.getScore() - 7 / (nearest_ghost_mandis + 1) - nearest_food_mandis/9
    

# Abbreviation
better = betterEvaluationFunction
