# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    
    
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)
        #static dictionary of Q-values, indexed by state
        QLearningAgent.qVals = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        #if this is the first time we see this state
        if QLearningAgent.qVals[state] == 0:
            #initialize dictionary of valid actions
            validActions = self.getLegalActions(state)
            #populate those actions with values 0.0
            QLearningAgent.qVals[state] = util.Counter(dict.fromkeys(self.getLegalActions(state), 0.0))
        if action == None:  #meaning I passed in a state to make sure it's initialized
            return 0.0
        return QLearningAgent.qVals[state][action]  #Q-value for that state-action pair

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        if QLearningAgent.qVals[state] == 0 or QLearningAgent.qVals[state] == {}:
            #unseen or terminal state
            return 0.0
        return max(QLearningAgent.qVals[state].values())

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        #best action for a state
        actions = QLearningAgent.qVals[state]
        if actions == {}:   #terminal state
            return None
        if actions == 0:    #means this is the first time the agent has seen this state; choose randomly
            return random.choice(self.getLegalActions(state))
        return QLearningAgent.qVals[state].argMax() #action with max q-value
        

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        #epsilon-greedy
        legalActions = self.getLegalActions(state)
        action = None
        if len(legalActions) == 0:  #no legal actions: Return None
            action = None
        if util.flipCoin(self.epsilon): #with probability < Epsilon
            action = random.choice(legalActions)    #Choose randomly
        else:
            action = self.computeActionFromQValues(state)   #Choose best policy action
        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        #Q(s, a) = Q(s, a) + alpha(r(t + 1) + gamma * max action(Q(nextS, nextA)) - Q(s, a)
        currentQ = self.getQValue(state, action) #if there isn't a q-value for this state, this function will initialize it
        initializeNextQ = self.getQValue(nextState, None) #make sure the next state is initialized in the table
        actualNextQ = self.discount * self.computeValueFromQValues(nextState) - currentQ #actual gamma * max Q(next) - Q(s, a)
        actualNextQ += reward   #add reward
        actualNextQ *= self.alpha   #multiply by learning rate
        actualNextQ += currentQ     #add current Q-value
        QLearningAgent.qVals[state][action] = actualNextQ   #put the updated Q-value back in the table
        

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action