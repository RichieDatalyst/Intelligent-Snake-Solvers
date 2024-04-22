import State
import agentsnake
import astar
import greedybestfirst
import breadthfirst
import view
import threading
import time

class Main:
    def __init__(self, State, AgentSnake, SnakeSpeed=30):
        self.State = State
        self.AgentSnake = AgentSnake
        self.View = view.SnakeViewer(self.State, SnakeSpeed)

    def setDirection(self, k):
        if k == 0:
            self.State.snake.HeadDirection.X = 0
            self.State.snake.HeadDirection.Y = -1
        elif k == 6:
            self.State.snake.HeadDirection.X = 0
            self.State.snake.HeadDirection.Y = 1
        elif k == 3:
            self.State.snake.HeadDirection.X = 1
            self.State.snake.HeadDirection.Y = 0
        elif k == 9:
            self.State.snake.HeadDirection.X = -1
            self.State.snake.HeadDirection.Y = 0

    def ExecutePlan(self, Plan):
        for k in Plan:
            self.setDirection(k)
            self.State.snake.moveSnake(self.State)
            if not self.State.snake.isAlive:
                break
            time.sleep(1 / self.View.SPEED)
            self.View.UpdateView()

    def StartSnake(self):
        if not self.State.snake.isAlive:
            return
        PlanIsGood = True
        Message = "Game Over"
        while self.State.snake.isAlive and PlanIsGood:
            ScoreBefore = self.State.snake.score
            Plan = self.AgentSnake.SearchSolution(self.State)
            self.ExecutePlan(Plan)
            ScoreAfter = self.State.snake.score
            if ScoreAfter == ScoreBefore:
                PlanIsGood = False
            self.State.generateFood()
            time.sleep(1/2)

        if self.State.snake.isAlive:
            Message = Message + "  HAS A BAD PLAN"
        else:
            Message = Message + " HAS HIT A WALL"
        self.View.ShowGameOverMessage(Message)

    def Play(self):
        t1 = threading.Thread(target=self.StartSnake)
        t1.start()
        t2 = threading.Thread(target=self.View.top.mainloop())
        t2.start()
        t1.join()
        t2.join()

def main():
    state = State.SnakeState('red', 10, 10, 0, 1, "Maze2.txt")
    agent = agentsnake.AgentSnake('AStar')  # Use the AgentSnake class from agentsnake module
    game = Main(state, agent)
    game.Play()

if __name__ == '__main__':
    main()
