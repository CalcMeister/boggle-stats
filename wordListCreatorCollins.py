from PyDictionary import PyDictionary

pydict = PyDictionary()
word_list = []
dict_lines = open("2019_Scrabble_Dictionary.txt","r").readlines()
removalTypes = ["having fewer than 4 letters.","being an \'es\' plural.","being an \'es\' plural.","being an \'ing\' adverb.","being an \'er\' noun/adjective.","being an \'est\'superlative adjective.","being a \'d\' past tense.","being an \'ed\' past tense."]
removalAmounts = [0]*10

open("Boggle_Dictionary.txt","w+")
file = open("Boggle_Dictionary.txt","a")

lengthLimit = int(input("Minimum word length: "))

print("There are 279,496 words in the supplied dictionary.")

dict_lines = list(line.strip().lower() for line in dict_lines)

for word in dict_lines:
	if len(word) < lengthLimit:
		print("Word removed. Fewer than 4 letters. Word: \""+word+"\"")
		removalAmounts[0] += 1
	elif word[len(word)-1] == "s":
		if word[0:len(word)-1] in dict_lines:
			print("Word removed. \'s\' Plural.           Word: \""+word+"\"")
			removalAmounts[1] += 1
		elif word[len(word)-2] == "e" and word[0:len(word)-2] in dict_lines:
			print("Word removed. \'es\' Plural.          Word: \""+word+"\"")
			removalAmounts[2] += 1
	elif word[len(word)-3:] == "ing" and (word[0:len(word)-3] in dict_lines or (word[0:len(word)-4] in dict_lines and word[len(word)-4] == word[len(word)-5]) or word[0:len(word)-3]+"e" in dict_lines):
		print("Word removed. \'ing\' adverb.         Word: \""+word+"\"")
		removalAmounts[3] += 1
	elif word[len(word)-2:] == "er" and (word[0:len(word)-2] in dict_lines or (word[0:len(word)-3] in dict_lines and word[len(word)-3] == word[len(word)-4])):
		print("Word removed. \'er\' noun/adjective.  Word: \""+word+"\"")
		removalAmounts[4] += 1
	elif word[len(word)-3:] == "est" and word[0:len(word)-3] in dict_lines:
		print("Word removed. \'est\' superlative.    Word: \""+word+"\"")
		removalAmounts[5] += 1
	elif word[len(word)-1] == "d":
		if word[0:len(word)-1] in dict_lines:
			print("Word removed. \'d\' past tense.       Word: \""+word+"\"")
			removalAmounts[6] += 1
		elif word[len(word)-2] == "e" and word[0:len(word)-2] in dict_lines:
			print("Word removed. \'ed\' past tense.      Word: \""+word+"\"")
			removalAmounts[7] += 1
	#elif pydict.meaning(word) == None:
	#	print("Word removed. Not in PyDictionary.  Word: \""+word+"\"")
	else:
		print("Word accepted.                      Word: \""+word+"\"")
		#word_list.append(word)
		file.write(word+"\n")

print("Deleted "+str(sum(removalAmounts))+" out of 279,496 words.")
for i in range(len(removalTypes)):
	print("Removed "+str(removalAmounts[i])+" words for "+removalTypes[i])










# t = 0
# accepted = 0
# total = len(english_words_set)
# for word in english_words_set:
# 	t = t+1
# 	if word[:1].isupper():
# 		print("Word removed. Proper noun.          Word: \""+word+"\"")
# 	elif "\'" in word:
# 		print("Word removed. Contraction.          Word: \""+word+"\"")
# 	elif len(word) <= 3:
# 		print("Word removed. Fewer than 4 letters. Word: \""+word+"\"")
# 	else:
# 		print("Word accepted.                     Word: \""+word+"\"")
# 		accepted = accepted+1
# 		file.write(word+"\n")

# print("Deleted "+str(total-accepted)+" out of "+str(total)+" words.")

	# if t >= 100:
	# 	break

# if "singe" in english_words_set:
# 	print("true")
# else:
# 	print("false")

# if "singer" in english_words_set:
# 	print("true")
# else:
# 	print("false")

