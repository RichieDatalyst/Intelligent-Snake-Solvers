from collections import deque

class BreadthFirst:
    def __init__(self, state):
        self.state = state

    def search(self):
        start = (self.state.snake.HeadPosition.X, self.state.snake.HeadPosition.Y)
        goal = (self.state.FoodPosition.X, self.state.FoodPosition.Y)
        frontier = deque()
        frontier.append(start)
        came_from = {}
        came_from[start] = None

        while frontier:
            current = frontier.popleft()

            if current == goal:
                break

            for next in self.state.getAdjacentNodes(current):
                if next not in came_from:
                    came_from[next] = current
                    frontier.append(next)

        path = self.reconstructPath(came_from, start, goal)
        actions = self.convertPathToActions(path)
        return actions

    def reconstructPath(self, came_from, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path

    def convertPathToActions(self, path):
        actions = []
        for i in range(1, len(path)):
            current = path[i]
            previous = path[i - 1]
            if current[0] > previous[0]:
                actions.append(3)  # Right
            elif current[0] < previous[0]:
                actions.append(9)  # Left
            elif current[1] > previous[1]:
                actions.append(6)  # Down
            elif current[1] < previous[1]:
                actions.append(0)  # Up
        return actions