import random
import copy
import sys
import os
from colorama import Fore, Back, Style, init
from PyDictionary import PyDictionary
pydict = PyDictionary()

class board:
	def __init__(self, diceList, dimensions):
		self.diceList = diceList
		self.columns = dimensions[0]
		self.rows = dimensions[1]
		self.arrangement = list(range(self.rows * self.columns))
		self.letterGrid = [[" " for i in range(self.columns)] for j in range(self.rows)]

	def shake(self):
		random.shuffle(self.arrangement)
		for d in self.diceList:
			d.roll()

		for i in range(self.rows):
			for j in range(self.columns):
				self.letterGrid[i][j] = self.diceList[self.arrangement[self.columns * i + j]].returnCurrentLetter()

		#self.letterGrid = [["k","s","c","h","t"],["y","h","a","t","n"],["g","e","i","s","he"],["n","a","e","e","h"],["f","r","t","e","r"]]

		return self.returnLetterGrid()

	def returnLetterGrid(self):
		return self.letterGrid

	def returnLetter(self, row, column):
		return self.letterGrid[row][column]

class die:
	def __init__(self, letters):
		self.letters = letters
		self.currentLetter = letters[0]

	def roll(self):
		self.currentLetter = self.letters[random.randrange(0,len(self.letters)-1)]
		return self.currentLetter

	def returnCurrentLetter(self):
		return self.currentLetter

def diceStringToList(string):
	return [die(j) for j in [i.split(" ") for i in string.split("\n")]]

def returnWordText(letterGrid, currentWord):
	#Returns the word text by combining a letter grid and currentWord.
	wordText = ""
	depth = max(max(i) for i in currentWord)
	for n in range(1,depth+1):
		for i in range(len(currentWord)):
			for j in range(len(currentWord[0])):
				if currentWord[i][j] == n:
					wordText += letterGrid[i][j]
	# printReadableArray(currentWord)
	# print(wordText)
	return wordText

def integerName(n):
	if n == 0:
		return "zero"
	name = ""
	denominations = ["","thousand","million","billion","trillion","quadrillion"]
	tens = ["","","twenty","thirty","forty","fifty","sixty","seventy","eighty","ninety"]
	ones = ["","one","two","three","four","five","six","seven","eight","nine"]
	teens = ["ten","eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen"]

	for i in range((len(str(n))+2)//3-1, -1, -1):
		if n//1000**i//100%10 != 0:
			name += ones[n//1000**i//100%10]+" hundred "
		if n//1000**i//10%10 >= 2:
			name += tens[n//1000**i//10%10]+" "
		if n//1000**i//10%10 == 1:
			name += teens[n//1000**i%10]+" "
		if n//1000**i%10 != 0 and n//1000**i//10%10 != 1:
			name += ones[n//1000**i%10]+" "
		if i != 0:
			name += denominations[i]+" "

	name = name[0:len(name)-1]
	return Fore.WHITE+name+Fore.RESET

def arrayMaximumIndex(array):
	return [list(max(i) for i in array).index(max(max(i) for i in array)),array[list(max(i) for i in array).index(max(max(i) for i in array))].index(max(array[list(max(i) for i in array).index(max(max(i) for i in array))]))]

def printReadableBoard(b):
	boardColor = Fore.BLUE+Back.WHITE+Style.BRIGHT
	print(boardColor, end="")
	for i in range(b.rows):
		for j in range(b.columns):
			print(boardColor+b.returnLetter(i,j).capitalize(), end=boardColor+" "[0:len(b.returnLetter(i,j)) == 1])
		print("\n", end="")

def printReadableArray(array):
	boardColor = Fore.BLUE+Back.WHITE
	print(boardColor, end="")
	for i in range(len(array)):
		for j in range(len(array[0])):
			print(boardColor+array[i][j], end=boardColor+" ")
		print("\"", end="")

def wordSearch(letterGrid, word, permList):
	#Will return True if word exists as a legal Boggle string in letterGrid. False if otherwise.
	def recursiveSearch(letterGrid, word, position, currentWord):
		localCurrentWord = copy.deepcopy(currentWord)
		localCurrentWord[position[0]][position[1]] = 0
		currentDepth = max(max(i) for i in localCurrentWord)+1
		localCurrentWord[position[0]][position[1]] = currentDepth
		wordExists = False

		# print("localCurrentWord:")
		# printReadableArray(localCurrentWord)

		if len(returnWordText(letterGrid, localCurrentWord)) >= len(word):
			wordExists = True
		else:
			for i in range(position[0]-1,position[0]+2):
				for j in range(position[1]-1,position[1]+2):
					if (i in range(len(localCurrentWord))) and (j in range(len(localCurrentWord[0]))) and localCurrentWord[i][j] == 0 and letterGrid[i][j] == word[len(returnWordText(letterGrid, localCurrentWord)):len(returnWordText(letterGrid, localCurrentWord))+len(letterGrid[i][j])]:
						if recursiveSearch(letterGrid, word, [i,j], localCurrentWord):
							wordExists = True
							return wordExists

		return wordExists

	#print("Searching for \""+word+"\"")

	wordExists = False

	for permutation in permList:
		if permutation[0] == word[:len(permutation[0])]:
			if recursiveSearch(letterGrid, word, arrayMaximumIndex(permutation[1]), permutation[1]):
				wordExists = True
				return wordExists


def generateWordList(letterGrid, dictionary):
	
	permList = generatePermutationList(letterGrid, 3)
	wordList = []
	permDict = generatePermutationDict(permList)

	for word in dictionary:
		if word[:3] in permDict:
			if wordSearch(letterGrid, word, (permList[i] for i in permDict[word[:3]])):
				if len(word) >= 10:
					print("Found a "+integerName(len(word))+" letter word!\n\""+word+"\"")
				wordList.append(word)
		elif word[:4] in permDict:
			if wordSearch(letterGrid, word, (permList[i] for i in permDict[word[:4]])):
				if len(word) >= 10:
					print("Found a "+integerName(len(word))+" letter word!\n\""+word+"\"")
				wordList.append(word)

	return wordList

def generatePermutationDict(permList):
	permDict = {}
	for p in permList:
		if p[0] not in permDict:
			permDict[p[0]] = [permList.index(p)]
		else:
			permDict[p[0]].append(permList.index(p))
	return permDict

def generatePermutationList(letterGrid, depth):
	def recursiveSearch(letterGrid, depth, position, currentWord, permList):
		#letterGrid is in the form of a two dimensional list, e.g. [["a","b"],["c","d",]]
		#
		#depth determines the length of the permutations in dice, not characters.
		#
		#position is in the form of a list [row,column]
		#
		#currentWord is also in the form of a two dimenstional list, but it contains ints
		#instead of strings. Each element of the list corresponds to an element in the
		#letter grid. A 0 means the letter has not yet been used in the permutation
		#branch. 1, 2, 3 and so on are used to show the first, second, and third dice
		#and so on of the current permutation branch. currentWord does not actually
		#contain any information about the letters in the word.
		#
		#permList is a list of lists, each sublist containing a string naming the letters
		#in the permutation and the associated currentWord array, as in
		#[["abc",currentWord],["def",currentWord]]
		#This is because duplicate permutations must be considered independently.

		# print("recursiveSearch(letterGrid, "+str(depth)+", "+str(position)+", currentWord, permList)")
		# print("currentWord:")
		# printReadableArray(currentWord)

		localPermList = []
		localCurrentWord = copy.deepcopy(currentWord)
		currentDepth = max(max(i) for i in localCurrentWord)+1
		localCurrentWord[position[0]][position[1]] = currentDepth

		# print("localCurrentWord:")
		# printReadableArray(localCurrentWord)
		# print("permList:")
		# for i in permList:
		# 	print("\""+str(i[0])+"\"")
		# 	printReadableArray(i[1])
		# print("\n")

		if currentDepth >= depth:
			wordText = returnWordText(letterGrid, localCurrentWord)
			localPermList.append([wordText,localCurrentWord])
		else:
			for i in range(position[0]-1,position[0]+2):
				for j in range(position[1]-1,position[1]+2):
					if (i in range(len(localCurrentWord))) and (j in range(len(localCurrentWord[0]))) and localCurrentWord[i][j] == 0:
						localPermList += recursiveSearch(letterGrid, depth, [i,j], localCurrentWord, localPermList)

		return localPermList

	permList = []
	#emptyCurrentWord = list([list([0 for i in range(len(letterGrid[0]))]) for j in range(len(letterGrid))])
	emptyCurrentWord = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]


	for i in range(len(letterGrid)):
		for j in range(len(letterGrid[0])):
			#print(emptyCurrentWord)
			permList += recursiveSearch(letterGrid, depth, [i,j], [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]], [])

	return permList

	#print("Found "+str(len(permutations))+" possible letter permutations using a "+str(depth)+" letter word length on a "+str(len(letterGrid))+" by "+str(len(letterGrid[0]))+" board.")


debugLetterGrid = [["a","b","c","d","e"],["f","g","h","i","j"],["k","l","m","n","o"],["p","q","r","s","t"],["u","v","w","x","y"]]

bigBoggleDiceString = "f r y s a i\nr y s y p i\nr r g v o w\na n g m n e\nt d h o d n\nr h h l o d\na a e e e e\ne g u e a m\nt e s c n c\ns e s u n s\nt o u o o t\nhe an in er qu th\ne c p i t s\nm t e t o t\ne t i l i s\nt i t e i i\nh n h w d o\nn d e a n n\nu w t n o o\nb b z j k x\nl p t e s i\nh d r o n l\na f a i r s\ne a e m e e\na r a s f a"
bigBoggleDice = diceStringToList(bigBoggleDiceString)
Big_Boggle = board(bigBoggleDice,[5,5])
Big_Boggle.shake()
permList = []
wordList = []
updatedPermList = False
newline = "\n"
print(Style.BRIGHT, end="")
init(autoreset = True)

print("Initializing dictionary...")
boggleDict = open("Boggle_Dictionary.txt","r").read().split("\n")

print("Starting Boggle statistics application shell. Use \'help\' for command definitions.\nThe default board is Big Boggle.")

query = [""]
while query[0] != "exit":
	query = input(">").lower()
	query = query.split()

	#Current commands: board, help, shake, dict, count, stats, permlist, search, wordlist

	if query[0] == "board":
		print("Current letter grid:\n")
		printReadableBoard(Big_Boggle)

	elif query[0] == "help":
		print("placeholder")

	elif query[0] == "clear":
		os.system('cls' if os.name == 'nt' else 'clear')

	elif query[0] == "shake":
		Big_Boggle.shake()
		print("Letter grid randomized.")
		updatedPermList = False

	elif query[0] == "dict":
		if len(query) > 1:
			if query[1] in boggleDict:
				print("Word IS legal. Definition:")
			else:
				print("Word IS NOT legal. Definition:")
			print(pydict.meaning(query[1]))
		else:
			print("Syntax: dict word")

	elif query[0] == "count":
		for i in range(int(query[1])):
			print(integerName(i))
		#print(integerName(234567890987654321))

	elif query[0] == "stats":
		if wordList == []:
			print("Word list is empty!")
		else:
			print(str(len(wordList))+" words exist on the current letter grid. Of these,")
			for i in range(4,max(len(j) for j in wordList)+1):
				if sum((len(k) == i) for k in wordList) == 1:
					print(integerName(sum((len(k) == i) for k in wordList))+" is a"+"n"[0:i == 11 or str(i)[:1] == "8"]+" "+integerName(i)+"-letter word")
				else:
					print(integerName(sum((len(k) == i) for k in wordList))+" are "+integerName(i)+"-letter words")

	elif query[0] == "permlist":
		if len(query) > 1:
			permListDepth = int(query[1])
			if len(query) > 2 and query[2] == "-d":
				permList = generatePermutationList(debugLetterGrid, permListDepth)
			else:
				permList = generatePermutationList(Big_Boggle.returnLetterGrid(), permListDepth)
				updatedPermList = True
			print("Found "+str(len(permList))+" possible letter permutations using a "+str(permListDepth)+" letter word length on a "+str(Big_Boggle.rows)+" by "+str(Big_Boggle.columns)+" board.")
		else:
			print("Syntax: permlist depth")

	elif query[0] == "search":
		if len(query) > 1:
			if not updatedPermList:
				print("Permutation list is not updated. creating 3 die permutation list.")
				permList = generatePermutationList(Big_Boggle.returnLetterGrid(), 3)
				updatedPermList = True
			if wordSearch(Big_Boggle.returnLetterGrid(), query[1], permList):
				print("Word IS in letter grid.")
			else:
				print("Word IS NOT in letter grid.")
			if query[1] in wordList:
				print("Word IS in word list.")
			elif wordList == []:
				print("Word IS NOT in word list. (Word list is empty.)")
			else:
				print("Word IS NOT in word list.")
			if query[1][:3] in generatePermutationDict(permList) or query[1][:4] in generatePermutationDict(permList):
				print("Word IS in permutation dictionary.")
			elif permList == []:
				print("Word IS NOT in permutation dictionary. (Dict is empty.)")
			else:
				print("Word IS NOT in permutation dictionary.")
		else:
			print("Syntax: search word")

	elif query[0] == "sim":
		if len(query) > 1:
			wordFreqDict = {}
			letterGridList = []
			wordListList =[]

			for i in range(int(query[1])):
				print("Calculating word list for board "+str(i))
				Big_Boggle.shake()
				printReadableBoard(Big_Boggle)
				letterGridList.append(Big_Boggle.returnLetterGrid())
				wordList = generateWordList(Big_Boggle.returnLetterGrid(), boggleDict)
				print("Found "+integerName(len(wordList))+" words on board "+str(i))
				wordListList.append(wordList)
				for word in wordList:
					if word in wordFreqDict:
						wordFreqDict[word] += 1
					else:
						wordFreqDict[word] = 1

			aggregateWordList = []
			for i in wordListList:
				for j in i:
					aggregateWordList.append(j)

			print(str(len(aggregateWordList))+" words were found among "+str(query[1])+" letter grids. Of these,")
			for i in range(4,max(len(j) for j in aggregateWordList)+1):
				if sum((len(k) == i) for k in aggregateWordList) == 1:
					print(integerName(sum((len(k) == i) for k in aggregateWordList))+" is a"+"n"[0:i == 11 or str(i)[:1] == "8"]+" "+integerName(i)+"-letter word")
				else:
					print(integerName(sum((len(k) == i) for k in aggregateWordList))+" are "+integerName(i)+"-letter words")
			print(newline)

			print("The top 25 most frequent words were")
			wordFreqDict_temp = copy.deepcopy(wordFreqDict)
			for i in range(25):
				print("\""+max(wordFreqDict_temp, key=wordFreqDict_temp.get)+"\", on "+integerName(max(wordFreqDict_temp.values()))+" board"+"s"[0:max(wordFreqDict_temp.values()) != 1])
				del wordFreqDict_temp[max(wordFreqDict_temp, key=wordFreqDict_temp.get)]
			print(newline)

			print("The most abundant board had "+integerName(max(len(i) for i in wordListList))+" words, while the most barren had only "+integerName(min(len(i) for i in wordListList))+".")
			print(newline)

			print("Exporting data to Boggle_Simulation.txt")
			open("Boggle_Simulation.txt","w").write("letterGridList = "+repr(letterGridList)+newline+"wordListList = "+repr(wordListList)+newline+"wordFreqDict = "+repr(wordFreqDict)+newline)
			print("Done.")

		else:
			print("Syntax: sim iterations")

	elif query[0] == "wordlist":
		if len(query) > 1:
			wordlistFilename = query[1]
		else:
			wordlistFilename = "wordlist.txt"
		wordList = generateWordList(Big_Boggle.returnLetterGrid(),boggleDict)
		print("Found "+str(len(wordList))+" legal words on the current letter grid.")
		open(wordlistFilename,"w+")
		with open(wordlistFilename,"a") as file:
			for word in wordList:
				file.write(word+"\n")
		print("Word list from current board based on Boggle_Dictionary.txt saved to "+wordlistFilename)


















