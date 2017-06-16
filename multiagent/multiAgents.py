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
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newCaps = successorGameState.getCapsules()

        "*** YOUR CODE HERE ***"
        # print successorGameState
        # print "newpos" + str(newPos) + '\n'
        # print "newfood"+ str(newFood) + '\n'
        # print "newGS" + str(newGhostStates)+ '\n'
        # print "nST" +str(newScaredTimes) +  '\n'
        # print "newCaps" + str(newCaps) + '\n'

        mD = manhattanDistance(newPos, ghostState.getPosition())
        #print "GSP"+str(ghostState.getPosition())
        fooddist = [manhattanDistance(newPos, foodloc) for foodloc in newFood.asList()]
        #capdist = [manhattanDistance(newPos, caploc) for caploc in newCaps]
        if fooddist == []:
          return successorGameState.getScore()
        minfood = min(fooddist)
        #mincap = min(capdist)
        states = 0
        states2 = 0
        states3 = 0
        states4 = 0
        if successorGameState.isWin():
          states4 = 10000
        if successorGameState.isLose():
          states4 = -10000
        if successorGameState.getPacmanPosition() == currentGameState.getPacmanPosition():
          states = -1000

        if len(successorGameState.getCapsules()) < len(currentGameState.getCapsules()):
          states2 = 1000
        if mD == 3:
          states3 = -1000
        if mD == 2:
          states3 = -5000
        if mD == 1:
          states3 = -20000

        #foodgreed = manhattanDistance(newPos, maxfood)
        if (min(newScaredTimes) > 1 or states2 == 1000):
          #print "IF STATEMENT RESULT:" + str(successorGameState.getScore() - mD + minfood*10 + states + states2)
          #state3 = 20000
          return successorGameState.getScore() + states3 - .5*minfood + states + states2 + states4

       # print "NON STATEMENT RESULT:" + str(successorGameState.getScore() + mD + minfood* 10 + states + states2)
        return successorGameState.getScore() + states3 - .5*minfood + states + states2 + states4

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

        def maxPlayer(depth, gameState):
          depth += 1
          if depth == self.depth:
            return self.evaluationFunction(gameState)
          if gameState.isWin():
            return self.evaluationFunction(gameState)
          if gameState.isLose(): 
            return self.evaluationFunction(gameState)
          stateValue = -float("inf")

          available = gameState.getLegalActions(0)
          for action in available:
            successor = gameState.generateSuccessor(0, action)
            #minPlayer(depth, gameState, agent)
            minAction = minPlayer(depth, successor, 1)
            stateValue = max(stateValue, minAction)

          return stateValue

        def minPlayer(depth, gameState, agent):
          #agent should always be some ghost, so 1 or higher, but never > (number of agents - 1) since pacman is 0 
          if gameState.isWin():
            return self.evaluationFunction(gameState)
          if gameState.isLose(): 
            return self.evaluationFunction(gameState)
          stateValue = float("inf")

          available = gameState.getLegalActions(agent)
          for action in available:
            if agent < (gameState.getNumAgents() - 1):
              successor = gameState.generateSuccessor(agent, action)
              nextGhostAction = minPlayer(depth, successor, agent + 1)
              stateValue = min(stateValue, nextGhostAction)
            else:
              successor = gameState.generateSuccessor(agent, action)
              maxAction = maxPlayer(depth, successor)
              stateValue = min(stateValue, maxAction)
          return stateValue

        available = gameState.getLegalActions(0)
        stateValue = -float("inf")
        maxAction = None
        for action in available:
          depth = 0
          successor = gameState.generateSuccessor(0, action)
          intermediateMax = minPlayer(depth, successor, 1)
          if intermediateMax > stateValue:
            stateValue = intermediateMax
            maxAction = action
        return maxAction




        






class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #ALPHA BETA PRUNING 
        #alpha should be some small number
        #beta is some large number
        #for max if our value we get is greater than the large number, we make that the new beta 
        #min is opposite

        def maxPlayer(depth, gameState, alpha, beta):
          depth += 1
          if depth == self.depth:
            return self.evaluationFunction(gameState)
          if gameState.isWin():
            return self.evaluationFunction(gameState)
          if gameState.isLose(): 
            return self.evaluationFunction(gameState)
          stateValue = -99999

          available = gameState.getLegalActions(0)
          for action in available:
            successor = gameState.generateSuccessor(0, action)
            #minPlayer(depth, gameState, agent)
            minAction = minPlayer(depth, successor, 1, alpha, beta)
            stateValue = max(stateValue, minAction)
            #ALPHA IS MAX's BEST OPTION
            #BETA IS MIN's BEST OPTION
            #we want to max our value, so if its greater than MIN's best option, return our value
            #must update our alpha to be our best option

            if stateValue > beta:
              return stateValue
            #print ("alphaMaxBeFORE" + str(alpha))
            alpha = max(alpha, stateValue)
            #print("alphaMAX" + str(alpha))

          return stateValue

        def minPlayer(depth, gameState, agent, alpha, beta):
          #agent should always be some ghost, so 1 or higher, but never > (number of agents - 1) since pacman is 0 
          if gameState.isWin():
            return self.evaluationFunction(gameState)
          if gameState.isLose(): 
            return self.evaluationFunction(gameState)
          stateValue = 99999

          available = gameState.getLegalActions(agent)
          for action in available:
            if agent < (gameState.getNumAgents() - 1):
              successor = gameState.generateSuccessor(agent, action)
              nextGhostAction = minPlayer(depth, successor, agent + 1, alpha, beta)
              stateValue = min(stateValue, nextGhostAction)
              if stateValue < alpha:
                return stateValue
              beta = min(beta, stateValue)
            else:
              successor = gameState.generateSuccessor(agent, action)
              maxAction = maxPlayer(depth, successor, alpha, beta)
              stateValue = min(stateValue, maxAction)
              if stateValue < alpha:
                return stateValue
              beta = min(beta, stateValue)
          #print(type(stateValue))
          return stateValue

        available = gameState.getLegalActions(0)
        stateValue = -99999
        alpha = -99999
        beta = 99999
        maxAction = None
        for action in available:
          depth = 0
          successor = gameState.generateSuccessor(0, action)
          intermediateMax = minPlayer(depth, successor, 1, alpha, beta)
          if intermediateMax > stateValue:
            stateValue = intermediateMax
            maxAction = action
          # if stateValue >= beta:
          #   return stateValue
          alpha = max(alpha, stateValue)
        #print str(maxAction)

        return maxAction

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
        def maxPlayer(depth, gameState):
          depth += 1
          if depth == self.depth:
            return self.evaluationFunction(gameState)
          if gameState.isWin():
            return self.evaluationFunction(gameState)
          if gameState.isLose(): 
            return self.evaluationFunction(gameState)
          stateValue = -float("inf")

          available = gameState.getLegalActions(0)
          for action in available:
            successor = gameState.generateSuccessor(0, action)
            #minPlayer(depth, gameState, agent)
            expAction = expected(depth, successor, 1)
            stateValue = max(stateValue, expAction)

          return stateValue

        def expected(depth, gameState, agent):
          #agent should always be some ghost, so 1 or higher, but never > (number of agents - 1) since pacman is 0 
          if gameState.isWin():
            return self.evaluationFunction(gameState)
          if gameState.isLose(): 
            return self.evaluationFunction(gameState)

          stateValue = 0


          available = gameState.getLegalActions(agent)
          for action in available:
            if agent < (gameState.getNumAgents() - 1):
              successor = gameState.generateSuccessor(agent, action)
              nextGhostAction = expected(depth, successor, agent + 1)
              stateValue += nextGhostAction / len(gameState.getLegalActions(agent))
            else:
              successor = gameState.generateSuccessor(agent, action)
              maxAction = maxPlayer(depth, successor)
              stateValue += maxAction / len(gameState.getLegalActions(agent))
          return stateValue

        available = gameState.getLegalActions(0)
        stateValue = -float("inf")
        maxAction = None
        for action in available:
          depth = 0
          successor = gameState.generateSuccessor(0, action)
          intermediateMax = expected(depth, successor, 1)
          if intermediateMax > stateValue:
            stateValue = intermediateMax
            maxAction = action
        return maxAction



def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <Basically just improved the evaluation function I wrote above;
       Main thing was changing the return statement to account for eating ghosts; 
       we want to eat the ghosts if they're scared. We lose a bit of functionality because we can't check
       successor states.>
    """
    "*** YOUR CODE HERE ***"
    #successorGameState = currentGameState.generatePacmanSuccessor(action)
    pacManPos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    Caps = currentGameState.getCapsules()

    fooddist = [manhattanDistance(pacManPos, foodloc) for foodloc in Food.asList()]
    # FoodList = Food.asList()
    # for foodloc in FoodList:
    #   distToFood = manhattanDistance(pacManPos, foodloc)
    # if not fooddist:
    #   closestfooddist = 0

    #mD = manhattanDistance(pacManPos, ghostState.getPosition())
    mD = 0
    ghostdists = []

    for ghost in GhostStates:
      ghostPos = ghost.getPosition()
      ghostdist = manhattanDistance(pacManPos, ghostPos)
      ghostdists.append(ghostdist)
    mD = min(ghostdists)
    #print "GSP"+str(ghostState.getPosition())
    #fooddist = [manhattanDistance(newPos, foodloc) for foodloc in newFood.asList()]
    #capdist = [manhattanDistance(newPos, caploc) for caploc in newCaps]
    if fooddist == []:
      return currentGameState.getScore()
    minfood = min(fooddist)
    #mincap = min(capdist)
    states = 0
    states2 = 0
    states3 = 0
    states4 = 0
    if currentGameState.isWin():
      states4 = 10000
    if currentGameState.isLose():
      states4 = -10000
    # if currentGameState.getPacmanPosition() == currentGameState.getPacmanPosition():
    #   states = -1000

    # if len(successorGameState.getCapsules()) < len(currentGameState.getCapsules()):
    #   states2 = 1000
    if mD == 3:
      states3 = -1000
    if mD == 2:
      states3 = -5000
    if mD == 1:
      states3 = -20000

    #foodgreed = manhattanDistance(newPos, maxfood)
    if (min(ScaredTimes) > 2 or states2 == 1000):
      #print "IF STATEMENT RESULT:" + str(successorGameState.getScore() - mD + minfood*10 + states + states2)
      #state3 = 20000
      return currentGameState.getScore() + -states3 - minfood + states + states2 + states4

   # print "NON STATEMENT RESULT:" + str(successorGameState.getScore() + mD + minfood* 10 + states + states2)
    return currentGameState.getScore() + states3 - minfood + states + states2 + states4



# Abbreviation
better = betterEvaluationFunction

