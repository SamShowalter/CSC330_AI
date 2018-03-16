from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM
import os
from cell import cell
from SudokuSolver import SudokuSolver
import time

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board

class SudokuUI(Frame):
	"""
	The Tkinter UI, responsible for drawing the board and accepting user input.
	"""
	def __init__(self,parent,game):
		self.game = game

		Frame.__init__(self,parent)
		self.parent = parent
		self.__initUI()

	def __initUI(self):
		self.parent.title("Sudoku Solver")
		self.pack(fill=BOTH)
		self.canvas = Canvas(self,
                             width=WIDTH,
                             height=HEIGHT)
		self.canvas.pack(fill=BOTH, side=TOP)

		solve_button = Button(self,
                              text="Start Solver",
                              #foreground = "gray",
                              cursor = "trek",
                              command=self._solve_game)
		solve_button.pack(fill=BOTH, side=BOTTOM)

		#Draw the grid and draw the game
		self.__draw_grid()
		self.__draw_game()


	def __draw_grid(self):
		"""
		Draws grid divided with blue lines into 3x3 squares
		"""
		for i in range(10):
			if (i % 3 == 0): 
				if self.game.solved:
					color = 'green'
				elif (not self.game.progress):
					color = 'red'
				else:
					color = "blue"
				width = 2
			else: 
				color = "gray"
				width = 1

			x0 = MARGIN + i * SIDE
			y0 = MARGIN
			x1 = MARGIN + i * SIDE
			y1 = HEIGHT - MARGIN
			self.canvas.create_line(x0, y0, x1, y1, fill=color, width = width)

			x0 = MARGIN
			y0 = MARGIN + i * SIDE
			x1 = WIDTH - MARGIN
			y1 = MARGIN + i * SIDE
			self.canvas.create_line(x0, y0, x1, y1, fill=color, width = width)

	def __draw_game(self):
		self.canvas.delete("numbers")
		for i in range(9):
			for j in range(9):
				#Center alignment
				center_x = MARGIN + j * SIDE + SIDE / 2 
				center_y = MARGIN + i * SIDE + SIDE / 2

				#Cell in question
				cell = self.game.Game[i][j]

				#If the cell is solved
				if (cell.solved):

					#For finalized cells
					self.canvas.create_text(center_x, center_y, text=cell.finalValue, fill="black",tags = "numbers", font = ("Arial",30))

				elif (cell.guessed):
					self.canvas.create_text(center_x, center_y, text=cell.guessedValue, fill="orange",tags = "numbers", font = ("Arial",30))


				#For unfinished cells with less than four options left
				else:
					if len(cell.cellOptions) <= 4:

						#Alignment list for corner looking logic
						alignment_list = [(-18,-16), (18,-16),(-18,16),(18,16)]

						#Show each option
						for optionIndex in range(len(cell.cellOptions)):
							x_loc = center_x + alignment_list[optionIndex][0]
							y_loc = center_y + alignment_list[optionIndex][1]

							self.canvas.create_text(x_loc, y_loc, text=list(cell.cellOptions)[optionIndex], fill="gray",tags = "numbers", font = ("Arial",15))
		self.canvas.update()

	def _solve_game(self):
		count = 0
		while(not self.game.solved):
			self.game.progress = False
			self.game._solve_game_run()
			self.__draw_grid()
			self.__draw_game()
			count += 1

			time.sleep(.2)

			if count > 0:
				return

		if (not self.game.progress):
			print("GAME CANNOT BE SOLVED TRADITIONALLY. MOVING TO GUESSING AND BACKTRACKING.")
			#self.game._educated_guess()
			self.game._print_game()
			
		if self.game.solved:
			print("SOLVED!!!")
			self.game._print_game()
			self.__draw_grid()
			return


if __name__ == '__main__':
	#Add game logic here

	#easy game
	game_board=[[0, 0, 1, 0, 0, 0, 8, 9, 0],
				[0, 2, 7, 0, 0, 9, 0, 5, 0],
				[0, 0, 4, 0, 8, 2, 0, 0, 0],
				[0, 6, 0, 9, 2, 0, 1, 4, 0],
				[0, 0, 0, 0, 5, 0, 0, 0, 0],
				[0, 9, 8, 0, 6, 1, 0, 3, 0],
				[0, 0, 0, 2, 1, 0, 4, 0, 0],
				[0, 1, 0, 7, 0, 0, 3, 6, 0],
				[0, 7, 9, 0, 0, 0, 2, 0, 0]]

	#medium game
	# game_board =   [[4, 0, 0, 0, 0, 0, 0, 2, 0],
	# 				[8, 0, 0, 7, 0, 9, 0, 0, 0],
	# 				[0, 1, 6, 3, 0, 0, 0, 0, 0],
	# 				[5, 0, 9, 0, 0, 0, 0, 1, 0],
	# 				[3, 7, 4, 2, 0, 1, 5, 8, 6],
	# 				[0, 8, 0, 0, 0, 0, 7, 0, 9],
	# 				[0, 0, 0, 0, 0, 7, 6, 3, 0],
	# 				[0, 0, 0, 8, 0, 5, 0, 0, 4],
	# 				[0, 9, 0, 0, 0, 0, 0, 0, 7]]



	#Hard game
	# game_board =   [[5, 9, 0, 0, 0, 7, 0, 8, 0],
	# 				[0, 0, 0, 5, 0, 0, 0, 0, 7],
	# 				[4, 1, 0, 8, 0, 0, 5, 0, 6],
	# 				[0, 0, 1, 3, 0, 0, 0, 0, 4],
	# 				[0, 0, 5, 0, 0, 0, 9, 0, 0],
	# 				[8, 0, 0, 0, 0, 4, 2, 0, 0],
	# 				[9, 0, 2, 0, 0, 3, 0, 4, 5],
	# 				[1, 0, 0, 0, 0, 5, 0, 0, 0],
	# 				[0, 5, 0, 4, 0, 0, 0, 6, 9]]



	game = SudokuSolver(game_board)
	
	root = Tk()
	sudokuUI = SudokuUI(root,game)
	root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
	root.mainloop()
