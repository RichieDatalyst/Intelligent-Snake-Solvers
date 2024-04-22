import heapq

class GreedyBestFirst:
    def __init__(self, state):
        self.state = state

    def search(self):
        start = (self.state.snake.HeadPosition.X, self.state.snake.HeadPosition.Y)
        goal = (self.state.FoodPosition.X, self.state.FoodPosition.Y)
        frontier = []
        heapq.heappush(frontier, (self.heuristic(start, goal), start))
        came_from = {}
        came_from[start] = None

        while frontier:
            current = heapq.heappop(frontier)[1]

            if current == goal:
                break

            for next in self.state.getAdjacentNodes(current):
                if next not in came_from:
                    came_from[next] = current
                    heapq.heappush(frontier, (self.heuristic(next, goal), next))

        path = self.reconstructPath(came_from, start, goal)
        actions = self.convertPathToActions(path)
        return actions

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

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