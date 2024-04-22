import State
import astar
import greedybestfirst
import breadthfirst

class Agent(object):
    def SearchSolution(self, state):
        return []

class AgentSnake(Agent):
    def __init__(self, search_algorithm='AStar'):
        super().__init__()
        self.search_algorithm = search_algorithm
        self.algorithms = {
            'AStar': astar.AStar,
            'GreedyBestFirst': greedybestfirst.GreedyBestFirst,
            'BreadthFirst': breadthfirst.BreadthFirst
        }

    def setSearchAlgorithm(self, algorithm):
        if algorithm in self.algorithms:
            self.search_algorithm = algorithm
        else:
            print("Invalid search algorithm!")

    def SearchSolution(self, state):
        algorithm_class = self.algorithms[self.search_algorithm]
        algorithm = algorithm_class(state)
        return algorithm.search()

    def showAgent(self):
        print("A Snake Solver By MB")

    def planPath(self, state):
        FoodX = state.FoodPosition.X
        FoodY = state.FoodPosition.Y

        HeadX = state.snake.HeadPosition.X
        HeadY = state.snake.HeadPosition.Y

        DR = FoodY - HeadY
        DC = FoodX - HeadX

        plan = []

        F = -1
        if DR == 0 and state.snake.HeadDirection.X * DC < 0:
            plan.append(0)
            F = 6

        if state.snake.HeadDirection.Y * DR < 0:
            plan.append(3)
            if DC == 0:
                F = 9
            else:
                DC = DC - 1
        Di = 6
        if DR < 0:
            Di = 0
            DR = -DR
        for i in range(0, int(DR)):
            plan.append(Di)
        Di = 3
        if DC < 0:
            Di = 9
            DC = -DC
        for i in range(0, int(DC)):
            plan.append(Di)
        if F > 0:
            plan.append(F)
            F = -1

        return plan
    
    def getAdjacentNodes(self, node):
     """
     Returns a list of adjacent nodes to a given node
     """
     x, y = node
     directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
     adjacent_nodes = []

     for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < self.maze.WIDTH - 1 and 0 <= new_y < self.maze.HEIGHT - 1 and self.maze.MAP[new_y][new_x] != -1:

            adjacent_nodes.append((new_x, new_y))
     return adjacent_nodes
