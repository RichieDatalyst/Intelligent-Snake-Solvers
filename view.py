import time
import tkinter
import random
import State as st
import agentsnake
import threading
import astar
import greedybestfirst
import breadthfirst
class SnakeViewer:
	"""
	A view of the snake state
	"""
	def __init__(self, state, SPEED = 60, UnitSize = 10):
	
		self.SPEED = SPEED  # Greater value here increases the speed of motion of the snakes	
		self.state = state
		self.top = tkinter.Tk()
	#	self.top.state("zoomed")
		self.UnitSize = UnitSize  
		self.CANVAS_WIDTH = state.maze.WIDTH*UnitSize  # Width of drawing canvas in pixels
		self.CANVAS_HEIGHT = state.maze.HEIGHT*UnitSize  # Height of drawing canvas in pixels
		self.CreateBaseView(self.CANVAS_WIDTH, self.CANVAS_HEIGHT, 'SNAKE AI AGENT')
		
	def CreateBaseView(self, width, height, title):
		"""
		Method to create a canvas that acts as a base for all the objects in the game
		"""
		self.top.minsize(width=width, height=height)
		self.top.title(title)
		self.canvas = tkinter.Canvas(self.top, width=width + 1, height=height + 1, bg='white')
		self.canvas.pack(padx=10, pady=10)
		self.ScoreBoard = self.CreateScoreBoard('green')
		self.AddMaze(self.state.maze)
		self.UpdateView()

	def CreateScoreBoard(self, color):
		"""
		Method to position score_board text on the canvas for each player
		"""
		x_offset = 0.05
		return self.canvas.create_text(x_offset * self.CANVAS_WIDTH, 0.01 * self.CANVAS_HEIGHT, text=('Score : ' + str(0)), anchor=tkinter.NW, font=("Times", 12, 'bold'), fill = color)
		
	def AddSnake(self, snake):
		x0 = snake.HeadPosition.X*self.UnitSize
		y0 = snake.HeadPosition.Y*self.UnitSize
		
		W = x0 + self.UnitSize
		H = y0 + self.UnitSize
		
		self.canvas.delete("snake")
		
		#snake.HeadDirection.show()
		if(snake.HeadDirection.X == 1 or snake.HeadDirection.X == -1):
			W = W + 3
		else:
			H = H + 3
		self.canvas.create_oval(x0, y0, W, H, fill=snake.Color, tags='snake')
	
	def AddFood(self, food):
		x0 = food.X*self.UnitSize
		y0 = food.Y*self.UnitSize
		W = x0 + self.UnitSize
		H = y0 + self.UnitSize
		self.canvas.delete("food")
		self.canvas.create_oval(x0, y0, W, H, fill='green', tags='food')
		
	def AddMaze(self, maze):
		Units = st.Const.UNIT_SIZE
		for i in range(59):
			for j in range(59):
				if(maze.MAP[j][i] == -1):
					self.canvas.create_rectangle(i*Units, j*Units, (i+1)*Units, (j+1)*Units, fill='red', tags='wall')
		WI = 6
		for i in range(1,maze.HEIGHT*Units -WI, WI-1):
			self.canvas.create_rectangle(0,i,WI+2,i+WI,fill = 'red', tags = 'wall')
			self.canvas.create_rectangle((maze.WIDTH)*Units - WI+2,i,maze.WIDTH*Units+2,i+WI,fill = 'red', tags = 'wall')

		for i in range(1,maze.WIDTH*Units, WI-1):
			self.canvas.create_rectangle(i,1,i+WI,WI,fill = 'red', tags = 'wall')
			self.canvas.create_rectangle(i,(maze.HEIGHT)*Units-WI,i+WI,maze.HEIGHT*Units,fill = 'red', tags = 'wall')
	
	def UpdateView(self):
		self.AddSnake(self.state.snake)
		self.AddFood(self.state.FoodPosition)
		self.UpdateScore()
	
	def UpdateScore(self):
		self.canvas.itemconfig(self.ScoreBoard, text='Score : ' + str(self.state.snake.score))

	def ShowGameOverMessage(self, Message):
		self.top.title(Message)