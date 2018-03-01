import numpy as np 
import pandas as pd 
import os
import operator

os.chdir("/Users/Sam/Documents/Depauw/04 Senior Year/Semester 2/AI/proj3_GeneticAlg/Tests")

class GeneticAlg():

	def __init__(self):
		self.readData()
		self.Fitness = -10**100
		#print(self.findValue())
		self.evolve(10, 100)

		#self.printCoefficients()



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
		# 		# self.Vars = np.array([1])
		# 		self.Vars = np.concatenate([np.array([1]),np.random.uniform(0,10,self.NumVars)])
		# 		# np.insert(self.Vars, np.random.uniform(0,10,))
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

		self.Array = [[1,3,-5,.43],
					  [3,-4,9,-1.4],
					  [-5,9,-12,-0.3],
					  [.43,1.4,0.3,-.23]]

		self.Vars = np.concatenate([np.array([1]),np.random.uniform(0,10,self.NumVars)])

		

	def printCoefficients(self):
		for i in range(len(self.Array)):
			for j in range(i,len(self.Array)):
				print(self.Array[i][j], sep = " ")

	def fitness(self, Coeffs):
		fitness = 0
		for i in range(len(self.Array)):
			for j in range(i,len(self.Array)):
				if j == 0:
					fitness = self.Array[i][j]
				else:
					fitness += self.Array[i][j] * Coeffs[i] * Coeffs[j]

		return fitness

	def createOffspring(self,dad,mom,generationSize):
		diffs = dad - mom

		newspawn = []
		for kid in range(generationSize):
			kid = []
			for i in range(self.NumVars + 1):
				kid.append(dad[i] + np.random.normal(0,abs(diffs[i])))
									
			newspawn.append(np.asarray(kid))

		return newspawn


	def getParents(self, spawn, fitness):
		dadIndex = max(range(len(fitness)), key=fitness.__getitem__)
		dadArr = spawn[dadIndex]

		#Delete the values for mom and dad
		if fitness[dadIndex] > self.Fitness:
			self.bestVars = dadArr
			self.Fitness = fitness[dadIndex]

		momArr = spawn[min(range(len(fitness)), key=fitness.__getitem__)]

		return dadArr, momArr

		

	def evolve(self,generationSize, generations):
		spawn = []

		#Create initial random offspring
		for offspring in range(generationSize):
			spawn.append(np.concatenate([np.array([1]),np.random.uniform(0,10,self.NumVars)]))

		#Generate the fitness of each child
		fitness = [self.fitness(coeffs) for coeffs in spawn]

		dadArr, momArr = self.getParents(spawn, fitness)

		# self.createOffspring(dadArr,momArr,generationSize)
		for i in range(generations):

			print(self.Fitness)
			#Generate children
			spawn = self.createOffspring(dadArr,momArr,generationSize)

		 	#Generate the fitness of each child
			fitness = [self.fitness(coeffs) for coeffs in spawn]

			dadArr, momArr = self.getParents(spawn, fitness)

		print(self.bestVars)


GeneticAlg()






