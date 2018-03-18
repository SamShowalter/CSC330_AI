from functools import reduce
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
		self.numLoops = 0
		self.numGuesses = 0
		self.numCorrections = 0

		self.status = "Waiting"
		self.method = "None"

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

			try:
				#Get filename
				filename = input().strip()

				#Read in all lines of data
				out = open(filename, "r")
				file =  out.readlines()
				out.close()

				#Initialize puzzle

				#Filter out all empty lines
				file = [line for line in file if line.strip()]

				#Show the array read in
				print("\nPUZZLE READ SUCCESSFULLY. MOVING TO UI WINDOW.\n")

				#Read in each line of data for array
				for i in range(len(file)):
			

			# 		#Initialize cell row
					cellRow = []

					#Formate data correctly
					row = str(file[i]).rstrip("\n")

					#Converts any float values to integers automatically
					row = [int(num) for num in row.strip().split(" ") if num.strip()]

					#Verify row is formatted correctly
					if len(row) != 9:
						print("\nERROR:\nEach line in the sudoku puzzle must be 9 chars long.\n")
						return

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

			except Exception as e:
				print("\nError! file read failed. See details and try another filename.\n")
				print(str(e) + "\n")

	#Check all items in a row to see what can be in existing cell
	def check_row(self, row, col):

		#Determine which cell_options to use
		cell = self.Game[row][col]

		# Get cell options
		cell_options = cell.cellOptions

		#If the cell gets solved mid-loop
		if cell.solved:
			return

		#Temp cells
		temp_cell_options = copy.deepcopy(cell_options)

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

				#If the temp cell is solved or a guess (both have a final value)
				if temp_cell.solved or temp_cell.guessed:
					temp_cell_options -= set([temp_cell.finalValue])
					cell_options -= set([temp_cell.finalValue])

				#If there is a not finalValue
				else:
					temp_cell_options -= temp_cell.cellOptions 

		self.updateCellProgress(cell,temp_cell_options)

		

	def check_col(self, row, col):

		#Determine which cell_options to use
		cell = self.Game[row][col]

		#If this cell is based off of another guess
		# if guess:
		# 	if not cell.guessed: 
		# 		cell.getGuessOptions()
		# 	cell_options = cell.guessedCellOptions

		# else:
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

				#If the temp cell is solved or a guess (both have a final value)
				if temp_cell.solved or temp_cell.guessed:
					temp_cell_options -= set([temp_cell.finalValue])
					cell_options -= set([temp_cell.finalValue])

				#If there is a not a finalValue
				else:
					temp_cell_options -= temp_cell.cellOptions 

		#Update the cell's progress
		self.updateCellProgress(cell,temp_cell_options)

	def check_square(self, row, col):

		#Get the correct grid
		square_x_grid = row//3 
		square_y_grid = col//3

		#Get cell_options to use
		cell = self.Game[row][col]
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
						#If the cell is solved or guessed, it has a final value
						if temp_cell.solved or temp_cell.guessed:
							temp_cell_options -= set([temp_cell.finalValue])
							cell_options -= set([temp_cell.finalValue])

						#If the cell does not have a final value
						else:
							temp_cell_options -= temp_cell.cellOptions 

		#Update cell progress
		self.updateCellProgress(cell,temp_cell_options)
		#print("Row:",row,"Col:",col,"Cell Options:",cell.cellOptions)


	#Update cell progress based on cell optiion findings
	def updateCellProgress(self,cell, temp_cell_options):

		#If there is only one option that the cell can be
		if len(cell.cellOptions) == 1:
			self.progress = True
			cell.solved = True
			cell.finalValue = list(cell.cellOptions)[0]

		#There exist unique items that the cell has to offer. Otherwise, no
		if len(temp_cell_options) > 0:
			self.progress = True
			cell.cellOptions = cell.cellOptions.intersection(temp_cell_options)

	#Check the puzzle to see if it is solved
	def _check_for_solution(self):

		#Check rows
		for row in range(len(self.Game)):
			vals_list = [cell_item.finalValue for cell_item in self.Game[row]]

			if sum(set(vals_list)) != 45 or set(vals_list) != set(range(1,10)):
				return False

		#Check columns
		transpose_sudoku = list(zip(*self.Game))		
		for col in range(len(transpose_sudoku)):
			vals_list = [cell_item.finalValue for cell_item in transpose_sudoku[col]]

			if sum(set(vals_list)) != 45 or set(vals_list) != set(range(1,10)):
				return False

		#Check grids
		for row in range(3):
			for col in range(3):
				vals_list = []
				for grid_row in range(row*3,(row+1)*3):
					for grid_col in range(col*3,(col+1)*3):
						vals_list.append(self.Game[grid_row][grid_col].finalValue)

				if sum(set(vals_list)) != 45 or set(vals_list) != set(range(1,10)):
					return False

		self._exit_sequence()
		self.solved = True

	#Print the game at the end
	def _print_game(self):
		for row in range(len(self.Game)):
			for col in range(len(self.Game[row])):
				print(self.Game[row][col].finalValue, end = " ")
			print()

	#Make an educated guess about a cell with two options
	#When the solver stagnates (move to backtracking)
	def _educated_guess(self):
		#Guessing at a new item
		self.status = "Guessing"

		for row in range(len(self.Game)):
			for col in range(len(self.Game[row])):

				#Assign cell to a variable
				cell = self.Game[row][col]

				#Determine if the cell is solved
				if cell.solved or cell.guessed:
					continue

				#If the cell has two cell options
				else:
					if len(cell.cellOptions)  == 2:
						#ADD TO number of guesses
						self.numGuesses += 1

						#Other information
						cell.guessed = True; 
						cell.finalValue = list(cell.cellOptions)[0]
						cell.cellOptions = cell.cellOptions - set([cell.finalValue])
						self.stack.append(cell)
						self.progress = True
						return
			
	#Check to see if a guess led to a failure		
	def _check_for_failure(self):
		for row in range(len(self.Game)):
			for col in range(len(self.Game[row])):
				cell = self.Game[row][col]

				# A cell has no more options but is not solved means solver failed
				if (len(cell.cellOptions) == 0) and self.solved == False:
					return True

		#If none are found, then the solver successfully found a solution
		return False

	#Exit sequence to resolve any potentials
	def _exit_sequence(self):
		self.status = "SOLVED!!!"
		self._print_game()
		for row in range(len(self.Game)):
			for col in range(len(self.Game[row])):
				cell = self.Game[row][col]
				cell.solved = True
				cell.potential = False
				cell.guess = False
				cell.corrected = False

	#Correct errors after the solver made a bad educated guess
	def _correct_errors(self):
		self.status = "Error Correcting"

		#Add to corrections
		self.numCorrections += 1

		#Other information
		cell = self.stack.pop()
		cell.finalValue = list(cell.cellOptions)[0]
		cell.solved = True

		#Reset other cells
		for row in range(len(self.Game)):
			for col in range(len(self.Game[row])):

				#Assign a cell to a variable
				temp_cell = self.Game[row][col]

				#Ignore variables that are solved or guesses
				if (temp_cell.potential and not temp_cell.guessed) or temp_cell.corrected:
					temp_cell.resetOptions()

		#Reset the cell to guessed
		if (len(self.stack) > 0):
			cell.potential = True
		cell.guessed = False
		cell.corrected = True

	#Orchestration function to solve the game
	def _solve_game_run(self):

		#Set game progress
		self.status = "Solving"

		#Initially set game to false
		self.progress = False

		#Update number of loops
		self.numLoops += 1

		#Check each cell
		for row in range(len(self.Game)):
			for col in range(len(self.Game[row])):

				#Assign a variable to the cell
				cell = self.Game[row][col]

				#If the sell is solved or guessed, skip it
				if cell.solved or cell.guessed:
					continue

				#If the cell does not yet have an official final value
				else:
					#If there was a guess, make all changes cells potential
					if len(self.stack) > 0:
						cell.potential = True

					#Check the items near the cell for solutions
					self.check_row(row,col)
					self.check_col(row,col)
					self.check_square(row,col)
					self._check_for_solution()

				#If there is a failure
				if(self._check_for_failure()):
					self._correct_errors()
					return
					






