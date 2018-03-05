import numpy as np 
import pandas as pd 
import os
from math import inf
import operator

os.chdir("/Users/Sam/Documents/Depauw/04 Senior Year/Semester 2/AI/proj3_GeneticAlg/Tests")

class GeneticAlg():

	def __init__(self, generationSize = 10, numGenerations = 100):
		self.readData()
		self.Fitness = -inf
		self.GenerationSize = generationSize
		self.NumGenerations = numGenerations
		#print(self.findValue())
		self.evolve(generationSize, numGenerations)

		#self.printCoefficients()

	#Reads data from a file
	def readData(self):
		print("Welcome to the genetic algorithm builder.\n" +
			  "Please enter a filename for a function you would like to solve.\n" +
			  "The file should start with the number (n) of lines, followed by a space\n" +
			  "and then a list of numbers to fill the array")
		
		# while(True):

		# 	try:

		# 		filename = input().strip()

		# 		file = open(filename, "r")

		# 		numVars = int(file.readline().strip())
		# 		self.NumVars = numVars
		# 		print(numVars)
		# 		# self.BestVars = np.array([1])
		# 		self.BestVars = np.concatenate([np.array([1]),np.random.uniform(0,10,self.NumVars)])
		# 		# np.insert(self.BestVars, np.random.uniform(0,10,))
		# 		#Get final Array
		# 		self.Array = []
		# 		for i in range(numVars + 1):
		# 			row = str(file.readline()).rstrip("\n")
		# 			row = [int(num) for num in row.split(" ")]
		# 			print(row)
		# 			self.Array.append(row)
		# 		print(self.Array)

		# 		print(findValue())

		# 	except Exception as e:
		# 		print("\nError! file read failed. See details and try another filename.\n")
		# 		print(str(e) + "\n")
		self.NumVars = 3

		self.Array = [[1,3,5,1],
					  [3,4,9,4],
					  [5,9,12,1],
					  [3,1,0.3,1]]

		self.BestVars = np.concatenate([np.array([1]),np.random.uniform(0,10,self.NumVars)]).astype(int)

	#Print coefficients to verify readData is working correctly
	def printCoefficients(self):
		for i in range(len(self.Array)):
			for j in range(i,len(self.Array)):
				print(self.Array[i][j], sep = " ")

	#Determine the fitness of the specific weights
	def fitness(self, Coeffs):
		fitness = 0
		for i in range(len(self.Array)):
			for j in range(i,len(self.Array)):
				if j == 0:
					fitness = self.Array[i][j]
				else:
					fitness += self.Array[i][j] * Coeffs[i] * Coeffs[j]

		return fitness

	#Pads binary string so that it is always 8 characters
	def padBinString(self,num):
		temp_str = str(bin(num))[2 :] 							# String of number
		final_string = '0' * (8 - len(temp_str)) + temp_str 	# zero-padding plus string number

		return final_string

	#Converts an array of values to a binary string
	def convertToBinary(self,arr):

		#Initialize variables and empty final string
		variables = arr[1:]
		final_var_string = ""

		#Iterate through variables
		for var in variables:
			#Add the padded binary string to final
			final_var_string += self.padBinString(var)

		return final_var_string

	#Convert a binary string to an integer array
	def convertBinToVars(self, kid):
		#Initialize array of all ones
		arr = np.array([1]*(len(self.BestVars)))

		#For each variable
		for var in range(1,len(self.BestVars)):
			arr[var] = int(kid[(var-1)*8:(var)*8], base = 2)

		return arr.astype(int)


	#Use combination to generate a child
	def generateChild(self, dad, mom):
		#Get middle index
		mid_index = len(dad) // 2

		# Get random number indices for each half
		mut_index_first_half = np.random.randint(0, mid_index)
		mut_index_second_half = np.random.randint(mid_index, len(dad))

		#Create two children with crossover
		kid1 = dad[: mut_index_first_half] + mom[mut_index_first_half:mut_index_second_half] + dad[mut_index_second_half:]
		kid2 = mom[: mut_index_first_half] + dad[mut_index_first_half:mut_index_second_half] + mom[mut_index_second_half:]

		#Store potential kids for future random choosing
		potential_kids = [kid1,kid2]

		#choose a random child from potential kids
		return potential_kids[np.random.randint(0,2)]

	#Mutate randomly in a population
	def mutate(self,spawn,oddsOfMutation, numChangeMult = 16):

		#For each child in the generation
		for offspring in range(self.GenerationSize):
			#Randomly choose a child
			randKid = np.random.randint(0,self.GenerationSize)

			#Potentially mutate that child based on the odds of mutation ()
			spawn[randKid] = self.mutateOne(spawn[randKid],oddsOfMutation, numChangeMult)

		return spawn


	#Mutate random children
	def mutateOne(self, kid, chanceRange, numChangeMult):

		#Initialize the number of changes to be made if mutation occurs
		numChanges = len(kid) // numChangeMult
		randomChance = np.random.randint(0,chanceRange)

		#Only do it if the random Chance equals
		if randomChance == 0:

			#Random number of mutation changes
			mutNum = np.random.randint(0,numChangeMult)

			#Mutate the child "changeNum" times
			for change in range(mutNum):
				#Random index
				randIndex = np.random.randint(0,len(kid))

				if kid[randIndex] == "1":
					kid = kid[:randIndex] + "0" + kid[randIndex:]
				else:
					kid = kid[:randIndex] + "1" + kid[randIndex:]

		#Put child back in population
		return kid


	#
	def createOffspring(self,dad,mom,generationSize):
		newspawn = []
		for kid in range(generationSize):
			newspawn.append(self.convertBinToVars(self.generateChild(dad,mom)))
									
		return newspawn

	def chooseParentIndex(self,fitChart):
		rNum = np.random.uniform(0,1)
		
		for i in range(len(fitChart)):
			if fitChart[i] >= rNum:
				return (i - 1)

		#If it was exactly one
		return len(fitChart) - 1

	#Cumulate (sum) distribution of fitnesses
	def getFitChart(self,fitnessPerc):
		fitChart = [fitnessPerc[0]]
		for i in range(1,len(fitnessPerc)):
			fitChart.append(sum(fitnessPerc[0:i+1]))

		return fitChart

	#Find the parents from a population probabilistically
	def getParents(self, spawn, fitness):

		#Get fitness percentages (all non negative)
		pos_fitness = [(fit + (abs(min(fitness)) + 1)) for fit in fitness]
		fitness_perc = (pos_fitness / sum(pos_fitness))

		#Get the fitness chart
		fit_chart = self.getFitChart(fitness_perc)
		#print(" ".join([str(i) for i in fitChart]))

		while(True):
			dadIndex, momIndex = self.chooseParentIndex(fit_chart), self.chooseParentIndex(fit_chart)
			if dadIndex != momIndex:
				return self.convertToBinary(spawn[dadIndex]), self.convertToBinary(spawn[momIndex])

		
	def evolve(self,generationSize, numGenerations):
		spawn = []

		#Create initial random offspring
		for offspring in range(generationSize):
			spawn.append(np.concatenate([np.array([1]),np.random.randint(0,256, size = self.NumVars)]))

		#Generate the fitness of each child
		fitness = [self.fitness(coeffs) for coeffs in spawn]

		#Pick parents randomly based on fitness
		dad, mom = self.getParents(spawn, fitness)

		#Evolve the sample 
		for generation in range(numGenerations):

			#Generate children
			#print(spawn)
			spawn = self.createOffspring(dad,mom,generationSize)
			spawn = self.mutate(spawn,5)

			# print(self.convertBinToVars(dad), self.convertBinToVars(mom))
			# print(" ".join([str(i) for i in spawn]))
			# print("\n\n\n\n\n")

		 	#Generate the fitness of each child
			fitness = [self.fitness(kid) for kid in spawn]

			#Regnerate parents
			if (max(fitness) > self.Fitness):
				#Update Fitness and variable values
				self.Fitness = max(fitness)
				self.BestVars = spawn[fitness.index(self.Fitness)]
				dad, mom = self.getParents(spawn, fitness)

			# else:
			# 	dad = self.mutateOne(dad, 1, 16)
			print(self.Fitness, self.BestVars)


GeneticAlg(generationSize = 10, numGenerations = 5)










