class cell():

	def __init__(self, input_val): 

		#Give cell options from 1 - 9
		self.cellOptions = set(range(1,10))

		#Determine if a cell is already solved or not
		if input_val > 0 and input_val < 10:
			self.solved = True
		else:
			self.solved = False

		#Give a random input value as the final Value (won't be shown)
		self.finalValue = input_val

		#boolean to tell if it is based on guessed value
		self.potential = False

		#Show corrected options
		self.corrected = False

		#Boolean if the cell is one that is guessed at
		self.guessed = False

	#Re-setting options if a wrong option is picked
	def resetOptions(self):
		self.finalValue = 0
		self.solved = False
		self.potential = False
		self.corrected = False
		self.guessed = False
		self.cellOptions = set(range(1,10))


