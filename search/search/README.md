Project description: https://bhrolenok.github.io/teaching/cs-3600-spr2019/project1/index.html

Python version 2.7

Search algorithms are written in search.py. (Depth-first, breadth-first, uniform-cost, A*)

Created a state representation to make Pacman's goal reaching all four corners of the maze in SearchAgents.py.

Implemented a non-trivial, consistent A* heuristic for the above problem in SearchAgents.py.

Created a consistent heuristic for A* to make Pacman eat all the dots as efficiently as possible, also in SearchAgents.py.

Implemented a greedy solution to make Pacman eat all the dots in SearchAgents.py.

This project can be run through the command line. Use these commands (from commands.txt) to see my work:

---
python pacman.py -l tinyMaze -p SearchAgent
python pacman.py -l mediumMaze -p SearchAgent
python pacman.py -l bigMaze -z .5 -p SearchAgent
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs
python pacman.py -l bigMaze -p SearchAgent -a fn=bfs -z .5
python eightpuzzle.py
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs
python pacman.py -l mediumDottedMaze -p StayEastSearchAgent
python pacman.py -l mediumScaryMaze -p StayWestSearchAgent
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic 
python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem
python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5
python pacman.py -l testSearch -p AStarFoodSearchAgent
python pacman.py -l trickySearch -p AStarFoodSearchAgent
python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5 
python pacman.py -l bigSearch -p ApproximateSearchAgent -z .5 -q
---
