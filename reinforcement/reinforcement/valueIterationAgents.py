# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        temp = util.Counter()   #to keep track of values while iterating
        #use this for argmax
        states = mdp.getStates()
        ValueIterationAgent.policy = dict.fromkeys(states, '')
        actionUtilities = {}
        #initialize utility fn
        for state in states:
            if mdp.isTerminal(state):
                self.values[state] = mdp.getReward(state)
            temp[state] = mdp.getReward(state)
        looper = 0
        #returns list of tuples - state and 
        # Write value iteration code here
        """
            U(s) = R(s) + Y * (max value after trying each action)(T(s, a, s') * U(s))
            Do this for all states
            Return policy
            Handle case for no available actions
        """
        #loop until we've hit the right number of iterations
        while looper < self.iterations:
            for state in states:
                actionUtilities = {}
                possibleActions = mdp.getPossibleActions(state)
                #start new Bellman eqn - add reward for each state
                if len(possibleActions) == 0:   #terminal state
                    newUtility = 0
                elif len(possibleActions) == 1: #1 possible action: exit
                    actionUtilities[possibleActions[0]] = self.computeQValueFromValues(state, possibleActions[0])
                    ValueIterationAgent.policy[state] = possibleActions[0]
                    newUtility = actionUtilities[possibleActions[0]]
                else:
                    for action in possibleActions:  #multiple possible actions; try them all
                        actionUtilities[action] = self.computeQValueFromValues(state, action)   #get the utility for each action at the given state
                    ValueIterationAgent.policy[state] = max(actionUtilities, key=actionUtilities.get)   #update the policy for this state
                    newUtility = actionUtilities[ValueIterationAgent.policy[state]]
                temp[state] = newUtility
            self.values = temp.copy()
            looper = looper + 1
        "*** YOUR CODE HERE ***"


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
          
          Utility of taking a certain action in a certain state
        """
        transitionProbs = self.mdp.getTransitionStatesAndProbs(state, action)
        #utility = P(making it to that state) * utility at that state
        utility = 0
        for nextState, probability in transitionProbs:
                utility =  utility + self.mdp.getReward(state) + (self.discount * (probability * self.getValue(nextState)))
        return utility
            
    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        if self.mdp.isTerminal(state):
            return None
        else:
            return ValueIterationAgent.policy[state]

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
