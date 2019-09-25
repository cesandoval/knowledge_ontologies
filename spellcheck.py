from textblob import Word

def spellcheck(word):
	word_object=Word(word)
	possibilities=word_object.spellcheck()

	if possibilities[0][1]>=.95:
		return possibilities[0][0]
	else:
		print('Inconclusive inputted text,'+word+ ' could be a variety of words')
		print (possibilities)
		return word
# print(spellcheck('rn'))
