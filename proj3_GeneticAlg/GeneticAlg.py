import numpy as np 
import os

os.chdir("/Users/Sam/Documents/Depauw/04 Senior Year/Semester 2/AI/proj3_GeneticAlg/Tests")

def readData():
	print("Welcome to the genetic algorithm builder.\n" +
		  "Please enter a filename for a function you would like to solve.\n" +
		  "The file should start with the number (n) of lines, followed by a space\n" +
		  "and then a list of numbers to fill the array")
	
	while(True):

		try:

			filename = input().strip()

			file = open(filename, "r")

			numLines = int(file.readline().strip())
			print(numLines)

			finalArray = []
			for i in range(numLines):
				row = str(file.readline()).rstrip("\n")
				row = [int(num) for num in row.split(" ")]
				print(row)
				finalArray.append(row)
			print(finalArray)

			return

		except Exception as e:
			print("\nError! file read failed. See details and try another filename.\n")
			print(str(e) + "\n")

readData()


