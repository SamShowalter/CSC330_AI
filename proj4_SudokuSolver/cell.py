class cell():

	def __init__(self, input_val): #rowLoc, colLoc, gridLoc):
		self.cellOptions = set(range(1,10))
		if input_val > 0 and input_val < 10:
			self.solved = True
		else:
			self.solved = False
		self.finalValue = input_val

		#For backtracking
		self.guessedCellOptions = []
		self.guessedFinal = input_val
		self.guessed = False
		self.guessedSolved = False
		self.row = -1
		self.col = -1
		self.square = -1

