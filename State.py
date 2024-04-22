"""
A comparison of search strategies for playing the snake game.

The basic skeleton of the puzzle is given that repeatedly generates food for the snake at randomly selected positions until the snake dies by hitting itself or the algorithm generates an empty list of moves and hence fails to find a path from the present position of the snake head to the food.

This puzzle is designed by Mirza Mubasher Baig from NUCES:FAST Lahore, Pakistan

The puzzle provides a basic skeleton for providing the snake interface and connects it with a default search algorithm.

Requirements:
Implement each of the six search strategies and provide multiple instances of the search algorithm for playing the game.

You are encouraged to create a multi-thread application that uses multiple instances of the puzzle running concurrently using different search strategies for comparison.
"""

import random

class Const:
    UNIT_SIZE = 10

class Vector:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def show(self):
        print("[", self.X, ", ", self.Y, "]")

    def Update(self, X, Y):
        self.X = X
        self.Y = Y

    def Add(self, Vec):
        self.X = self.X + Vec.X
        self.Y = self.Y + Vec.Y

class Maze:
    def __init__(self, PuzzleFileName):
        self.MAP = []
        self.LoadMaze(PuzzleFileName)

    def LoadMaze(self, filename):
        with open(filename, 'r') as f:
            line = f.readline()
            [self.HEIGHT, self.WIDTH] = [int(digit) for digit in line.split()]
            self.MAP = [[int(digit) for digit in line.split()] for line in f]

class Snake:
    def __init__(self, Color, HeadPositionX=10, HeadPositionY=10, HeadDirectionX=1, HeadDirectionY=0):
        self.Size = 1
        self.Body = []  # in this implementation the body is empty
        self.Color = Color
        self.HeadPosition = Vector(HeadPositionX, HeadPositionY)
        self.HeadDirection = Vector(HeadDirectionX, HeadDirectionY)
        self.score = 0
        self.isAlive = True

    def moveSnake(self, State):

        if self.isAlive == False:
            return

        self.HeadPosition.Add(self.HeadDirection)

        r = self.HeadPosition.Y
        c = self.HeadPosition.X

        # Check for collisions with blocked areas and food
        # Is this the right place for this code?

        if (r >= State.maze.HEIGHT or r < 0) or (c >= State.maze.WIDTH or c < 0):
            self.isAlive = False
        elif State.maze.MAP[r][c] == -1:
            self.isAlive = False
        elif c == State.FoodPosition.X and r == State.FoodPosition.Y:
            self.score = self.score + 10

class SnakeState():
    def __init__(self, Color, HeadPositionX, HeadPositionY, HeadDirectionX, HeadDirectionY, mazeFileName):
        self.snake = Snake(Color, HeadPositionX, HeadPositionY, HeadDirectionX, HeadDirectionY)
        self.maze = Maze(mazeFileName)
        self.generateFood()

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

    def generateFood(self):
        """
        Method to randomly place a circular 'food' object anywhere on Canvas.
        The tag on it is used for making decisions in the program.
        """
        FoodFlag = False
        while (FoodFlag == False):
            x = random.randrange(3, self.maze.WIDTH - 3)
            y = random.randrange(3, self.maze.HEIGHT - 3)

            if self.maze.MAP[y][x] != -1:
                FoodFlag = True

        self.FoodPosition = Vector(x, y)