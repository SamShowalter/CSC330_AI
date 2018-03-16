import os
from cell import cell
import copy
import time

#Change to your own working directory
os.chdir("/Users/Sam/Documents/Depauw/04_Senior_Year/Semester_2/AI/proj4_SudokuSolver/Tests")

class SudokuSolver():


	#Constructor
	def __init__(self, game_board):
		self.Game = self.readData(game_board)
		self.solved = False
		self.progress = True

		#If stack is not empty, guessing == True
		self.stack = []
		
	#Reads data from a file
	def readData(self, game):
		print("Welcome to the Sukdoku Solver.\n" +
			  "Please enter a filename for a game you would like to solve.\n" +
			  "The file should have nine rows and nine columns of numbers from 0 - 9\n" +
			  "(zero represents empty) to fill the puzzle\n")

		while(True):

			final_game = []

			# try:
			# 	#Get filename
			# 	filename = input().strip()

			# 	#Read in all lines of data
			# 	out = open(filename, "r")
			# 	file =  out.readlines()
			# 	out.close()

			# 	#Initialize puzzle

			# 	#Filter out all empty lines
			# 	file = [line for line in file if line.strip()]

			# 	#Show the array read in
			# 	print("\nPUZZLE READ SUCCESSFULLY. MOVING TO UI WINDOW.\n")

			# 	#Read in each line of data for array
			# 	for i in range(len(file)):
			for row in game:

			# 		#Initialize cell row
				cellRow = []

			# 		#Formate data correctly
			# 		row = str(file[i]).rstrip("\n")

			# 		#Converts any float values to integers automatically
			# 		row = [int(num) for num in row.strip().split(" ") if num.strip()]

			# 		#Verify row is formatted correctly
			# 		if len(row) != 9:
			# 			print("\nERROR:\nEach line in the sudoku puzzle must be 9 chars long.\n")
			# 			return

				#For each number make sure valid input
				for number in row:
					if (number < 0) or (number > 9):
						print("\nERROR:\nValid characters for a sudoku puzzle must be in 0-9.\n")
						return
					#Create cell for that number
					else:
						cellRow.append(cell(number))

	            #If it passes all tests, add the row
				final_game.append(cellRow)

			#Make sure board is correct length
			if len(game) != 9:
				print("\nERROR:\nEach sudoku puzzle must be 9 lines long.\n")
				return

			return final_game

			# except Exception as e:
			# 	print("\nError! file read failed. See details and try another filename.\n")
			# 	print(str(e) + "\n")

	def check_row(self, row, col, guess = False):

		#Determine which cell_options to use
		cell = self.Game[row][col]

		#If this cell is based off of another guess
		if guess:
			cell_options = cell.guessedCellOptions
			cell.guessed = True
		else:
			cell_options = cell.cellOptions

		#If the cell gets solved mid-loop
		if cell.solved:
			return

		#Temp cells
		temp_cell_options = copy.deepcopy(self.Game[row][col].cellOptions)

		#print("\n\nRows:")
		#Check cells in the row
		for col_num in range(len(self.Game[row])):
			#print(row,col_num)

			#Assign temp cell
			temp_cell = self.Game[row][col_num]

			#Do not look at itself, doesn't make sense
			if col_num == col:
				continue

			#If the cell is not itself
			else:

				if temp_cell.guessed:
					print("Broken")
					#Remove all solved values
					if temp_cell.guessedSolved:
						temp_cell_options -= set([temp_cell.guessedFinal])
						cell_options -= set([temp_cell.guessedFinal])
					else:
						temp_cell_options -= temp_cell.guessedCellOptions 

					#There is a winner
	
				#If the cell was not guessed
				else:
						#Remove all solved values
					if temp_cell.solved:
						temp_cell_options -= set([temp_cell.finalValue])
						cell_options -= set([temp_cell.finalValue])
					else:
						temp_cell_options -= temp_cell.cellOptions 

				#self.updateCellProgress(cell,temp_cell_options)

		

	def check_col(self, row, col, guess = False):

		#Determine which cell_options to use
		cell = self.Game[row][col]

		#If this cell is based off of another guess
		if guess:
			cell_options = cell.guessedCellOptions
			cell.guessed = True
		else:
			cell_options = cell.cellOptions

		#If the cell gets solved mid-loop
		if cell.solved:
			return

		#temp cell options
		temp_cell_options = copy.deepcopy(cell_options)

		#print("\n\nCols:")
		#Check cells in the column
		for row_num in range(len(self.Game)):
			#print(row_num, col)

			#Assign variable name to temp cell
			temp_cell = self.Game[row_num][col]

			#Do not look at itself, doesn't make sense
			if row_num == row:
				continue

			#If the cell is not itself
			else:

				if temp_cell.guessed:
					print("Broken")
					#Remove all solved values
					if temp_cell.guessedSolved:
						temp_cell_options -= set([temp_cell.guessedFinal])
						cell_options -= set([temp_cell.guessedFinal])
					else:
						temp_cell_options -= temp_cell.guessedCellOptions 

					#There is a winner
	
				#If the cell was not guessed
				else:
					#Remove all solved values
					if temp_cell.solved:
						temp_cell_options -= set([temp_cell.finalValue])
						cell_options -= set([temp_cell.finalValue])
					else:
						temp_cell_options -= temp_cell.cellOptions 

				#self.updateCellProgress(cell,temp_cell_options)

	def check_square(self, row, col, guess = False):

		square_x_grid = row//3 
		square_y_grid = col//3

		#Determine which cell_options to use
		cell = self.Game[row][col]
		if guess:
			cell_options = cell.guessedCellOptions
			cell.guessed = True
		else:
			cell_options = cell.cellOptions

		#If the cell gets solved mid-loop
		if cell.solved:
			return

		#Cell options
		temp_cell_options = copy.deepcopy(cell_options)

		#print("\n\nSquare:")
		#Check cells in the column
		for row_cell in range(3*square_x_grid, 3*(square_x_grid + 1)):
			for col_cell in range(3*square_y_grid, 3*(square_y_grid + 1)):
				#print(row_cell,col_cell)

				#Assign variable as temp cell
				temp_cell = self.Game[row_cell][col_cell]

				#Do not look at itself, doesn't make sense
				if row_cell == row and col_cell == col:
					continue

				#If the cell is not itself
				else:

					if temp_cell.guessed:
						print("Broken")
						#Remove all solved values
						if temp_cell.guessedSolved:
							temp_cell_options -= set([temp_cell.guessedFinal])
							cell_options -= set([temp_cell.guessedFinal])
						else:
							temp_cell_options -= temp_cell.guessedCellOptions 
		
					#If the cell was not guessed
					else:
							#Remove all solved values
						if temp_cell.solved:
							temp_cell_options -= set([temp_cell.finalValue])
							cell_options -= set([temp_cell.finalValue])
						else:
							temp_cell_options -= temp_cell.cellOptions 

					self.updateCellProgress(cell,temp_cell_options)
					print("Row:",row,"Col:",col,"Cell Options:",cell.cellOptions)


	#Update cell progress based on cell optiion findings
	def updateCellProgress(self,cell, temp_cell_options):

		if not cell.guessed:
			if len(cell.cellOptions) == 1:
				self.progress = True
				cell.solved = True
				cell.finalValue = list(cell.cellOptions)[0]


			#There exist unique items that the cell has to offer. Otherwise, no
			if len(temp_cell_options) > 0:
				self.progress = True
				cell.cellOptions = cell.cellOptions.intersection(temp_cell_options)

		else:
			print("Broken")
			if len(cell.guessedCellOptions) == 1:
				self.progress = True
				cell.guessedSolved = True
				cell.guessedValue = list(cell.guessedCellOptions)[0]


			#There exist unique items that the cell has to offer. Otherwise, no
			if len(temp_cell_options) > 0:
				self.progress = True
				cell.guessedCellOptions = cell.guessedCellOptions.intersection(temp_cell_options)

	def _check_for_solution(self):
		for row in range(len(self.Game)):
			for col in range(len(self.Game[row])):
				if not self.Game[row][col].solved:
					self.solved = False
					return

		self.solved = True

	def _print_game(self):
		for row in range(len(self.Game)):
			for col in range(len(self.Game[row])):
				print(self.Game[row][col].finalValue, end = " ")
			print()

	def _educated_guess(self):
		for row in range(len(self.Game)):
			for col in range(len(self.Game[row])):
				cell = self.Game[row][col]
				if cell.solved:
					continue
				else:
					if len(cell.cellOptions)  == 2:
						cell.guessedFinal = list(cell.cellOptions)[0]
						cell.guessedCellOptions = cell.cellOptions - set([cell.guessedFinal])
						cell.row = row
						cell.col = col
						cell.grid = (row//3,col//3)
						cell.guessed = True
						cell.guessedSolved = True
						self.stack.append(cell)


	def _solve_game_run(self):
		for row in range(len(self.Game)):
			for col in range(len(self.Game[row])):
				cell = self.Game[row][col]
				if cell.solved:
					print(cell.finalValue)
					continue
				else:
					if len(self.stack) == 0:
						self.check_row(row,col, guess = False)
						self.check_col(row,col, guess = False)
						self.check_square(row,col, guess = False)
						self._check_for_solution()

					else:
						print("False")
						self.check_row(row,col, guess = True)
						self.check_col(row,col, guess = True)
						self.check_square(row,col, guess = True)
						self._check_for_solution()
			return





