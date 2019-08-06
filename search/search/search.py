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
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()

def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    
    """
    Pseudocode:
    closed = {} (visited)
    open = {init} (frontier)
    current = init
    while (current != goal) && open != {})
        closed += current
        A = actions(current)
        open -= current, += [successors(current) - closed]
        current = open.pop
    if (isGoal(current)
        return actionSequence(current, init)    (parent backtrace)
    else
        return failure
    """
    from util import Stack
    sequence = []
    closed = []
    open = Stack()
    open.push([problem.getStartState(), [], 0])
    print open.list
    start = problem.getStartState()
    curr = [start, sequence, 0]
    while problem.isGoalState(curr[0]) == False and open.isEmpty() == False:
        #put curr in closed list
        closed.append(curr)
        #get successors
        validSuccessors = problem.getSuccessors(curr[0])
        #put valid successors in open
        for x, y, z in validSuccessors:
            flag = False
            #if successor's coordinates in closed, then don't add to open
            for i in range(len(closed)):
                if x in closed[i]:
                    flag = True
            if flag == False:
                #push successor and add action to list of actions to get there
                open.push([x, curr[1] + [y], z])
        #new curr
        curr = open.pop()
    if problem.isGoalState(curr[0]):
        return curr[1]
        

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    from util import Queue
    sequence = []
    closed = []
    open = Queue()
    open.push([problem.getStartState(), [], 0])
    start = problem.getStartState()
    curr = [start, sequence, 0]
    counter = 0
    while problem.isGoalState(curr[0]) == False and open.isEmpty() == False:
        curr = open.pop()
        #moving goal state check up here prevents us from expanding the goal node
        if problem.isGoalState(curr[0]):
            return curr[1]
        #put curr in closed list
        closed.append(curr)
        #get successors
        validSuccessors = problem.getSuccessors(curr[0])
        #put valid successors in open
        for x, y, z in validSuccessors:
            flag = False
            #if successor's coordinates in closed, then don't add to open
            for i in range(len(closed)):
                if x in closed[i]:
                    flag = True
            #...or if coordinates already in open, don't re-add
            for j in range(len(open.list)):
                if x in open.list[j]:
                    flag = True
            if flag == False:
                #push successor and add action to list of actions to get there
                open.push([x, curr[1] + [y], z])

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    #put neighbors in priority queue,
    #move to least cost neighbor, check if their neighbors are in queue or closed
    #if yes, update cost if necessary
    #if no, enqueue
    #repeat until done
    from util import PriorityQueue
    sequence = []
    closed = []
    open = PriorityQueue()
    open.push([problem.getStartState(), [], 0], 0)
    start = problem.getStartState()
    curr = [start, sequence, 0]
    counter = 0
    while problem.isGoalState(curr[0]) == False and open.isEmpty() == False:
        curr = open.pop()
        #moving goal state check up here prevents us from expanding the goal node
        if problem.isGoalState(curr[0]):
            return curr[1]
        #put curr in closed list
        closed.append(curr)
        #get successors
        validSuccessors = problem.getSuccessors(curr[0])
        #put valid successors in open
        for x, y, z in validSuccessors:
            flag = False
            inOpen = False
            inClosed = False
            oldCostClosed = 0
            oldCostOpen = 0
            newCost = curr[2] + z
            ind = 0
            ind1 = 0
            #if successor's coordinates in closed, then don't add to open
            for i in range(len(closed)):
                if x in closed[i]:
                    ind = i
                    oldCostClosed = closed[i][2]
                    inClosed = True
            #...or if coordinates already in open, don't re-add
            for a, b, c in open.heap:
                if x in c:
                    ind1 = c.index(x)
                    oldCostOpen = c[2]
                    inOpen = True
            if inOpen == False and inClosed == False:
                #push successor and add action to list of actions to get there
                open.push([x, curr[1] + [y], newCost], newCost)
            elif inOpen == True:
                #should re-push with new priority - can't take old items out
                #according to util.py
                if oldCostOpen > newCost:
                    open.push([x, curr[1] + [y], newCost], newCost)
            elif inClosed == True:
                if oldCostClosed > newCost:
                    closed[ind][1] = closed[ind][1] + [y]
                    closed[ind][2] = newCost
        counter = counter + 1
    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    """
    g = actual cost to node (lowest found)
    h = optimistic cost to goal (from heuristic(state, problem))
    while not empty(open):
        pop node with lowest f = g + h
        if isGoal, return path
        for node s in successors
            f' = g + 
    """
    from util import PriorityQueue
    sequence = []
    closed = []
    open = PriorityQueue()
    open.push([problem.getStartState(), [], 0], 0)
    start = problem.getStartState()
    curr = [start, sequence, 0]
    counter = 0
    while problem.isGoalState(curr[0]) == False and open.isEmpty() == False:
        curr = open.pop()
        #moving goal state check up here prevents us from expanding the goal node
        if problem.isGoalState(curr[0]):
            return curr[1]
        #put curr in closed list
        closed.append(curr)
        #get successors
        validSuccessors = problem.getSuccessors(curr[0])
        #put valid successors in open
        for x, y, z in validSuccessors:
            flag = False
            inOpen = False
            inClosed = False
            oldCostClosed = 0
            oldCostOpen = 0
            #new cost = cost of current node + cost of successor
            #this is g(successor)
            newCost = curr[2] + z
            ind = 0
            ind1 = 0
            #if successor's coordinates in closed, then don't add to open
            for i in range(len(closed)):
                if x in closed[i]:
                    ind = i
                    oldCostClosed = closed[i][2]
                    inClosed = True
            #...or if coordinates already in open, don't re-add
            for a, b, c in open.heap:
                if x in c:
                    ind1 = c.index(x)
                    oldCostOpen = c[2]
                    inOpen = True
            if inOpen == False and inClosed == False:
                #push successor and add action to list of actions to get there
                #priority = g(s) + h(s)
                open.push([x, curr[1] + [y], newCost], newCost + heuristic(x, problem))
            elif inOpen == True:
                #should re-push with new priority - can't take old items out
                #according to util.py
                #item already in open list but new lowest cost found
                if oldCostOpen > newCost:
                    open.push([x, curr[1] + [y], newCost], newCost + heuristic(x, problem))
            elif inClosed == True:
                if oldCostClosed > newCost:
                    closed[ind][1] = closed[ind][1] + [y]
                    closed[ind][2] = newCost
        counter = counter + 1
    


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
