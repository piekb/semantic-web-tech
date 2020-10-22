#DEBUG TERMS
DEBUG = True
DEBUG_SPACY = False

#IMPORTS AND GLOBAL VARIABLES
import sys, requests, spacy, itertools, operator, re
nlp = spacy.load("en")
urlQuery = "https://query.wikidata.org/sparql"
queryTemplate = """SELECT ?answer ?answerLabel WHERE {
		wd:%s wdt:%s ?answer .
		SERVICE wikibase:label {bd:serviceParam wikibase:language "en"}
		}"""
urlConvert = "https://www.wikidata.org/w/api.php"
paramsQ = {"action":"wbsearchentities", "language":"en", "format":"json"}
paramsP = {"action":"wbsearchentities", "language":"en", "format":"json", "type":"property"}

#ANSWER GENERATING SETTINGS
numberOfUsedP = 3
numberOfUsedQ = 9

#PRINT SOME EXAMPLE QUESTIONS
def printExamples():
	print("Example questions about geography:")
	print("\tWhat is the capital of the Netherlands?")
	print("\tWhat is the highest point of Russia?")
	print("\tWhat is the official language of Chile?")
	print("\tWhat ingredients does soup consist of?")
	print("\tList the timezones of Syria.")
	print("\tTell me the population of Monaco.")
	print("\tList the ingredients of paella.")
	print("Example questions about other stuff:")
	print("\tTell me who the president of America is.")
	print("\tList the colors of apples.")
	print("\tWho is owner of Audi?")
	print("Enter new question below. CTRL+C to exit.")
	print("Depending on the formulation, it usually answers within 20 seconds.\n")

#CLEAN THE INPUT
def cleanInput(line):
	line = line.rstrip()			#remove newline
	line = line.replace("?","") 	#remove question marks
	line = line.replace("!","") 	#remove exclamation marks
	line = line.replace(".","") 	#remove dots
	line = line.replace(",","") 	#remove commas
	line = line.replace("'","") 	#remove apostrophes
	line = line.replace('"','') 	#remove apostrophes
	return line

#FILTER WORDS FROM INPUT
def filterInput(line):
	line = line.lower()
	filterWords = ["a", "an" ,"what", "which", "who", "is", "the", "are", "give", "list", "many", "much", "how", "name", "all"]
	lineList = line.split(" ")
	lineFiltered = [word for word in lineList if word not in filterWords]
	line = " ".join(lineFiltered)
	return line

#DETERMINE TERMS WITH SPACY
def runSpacy(line):
	nouns = []
	terms = []
	finalTerms = []
	spacy = nlp(line)
	for chunk in spacy.noun_chunks:
		nouns.append(str(chunk.text))
	for noun in nouns:
		temp = []
		doc = nlp(noun)
		for token in doc:
			if token.lemma_ != "-PRON-":		#fixes some weird spaCy <v2 issue
				temp.append(token.lemma_)
		temp = " ".join(temp)
		terms.append(temp)
	for w in spacy:
		if DEBUG_SPACY:
			print(w.orth_ + "\t-->\ttag:" + w.tag_ + "\tpos:"+w.pos_ + "\thead:"+w.head.orth_, "\tdep:" + w.dep_ + "\tlemma:"+w.lemma_, sep="")
	ents = [e.lemma_ for e in spacy.ents]
	terms = [filterInput(term) for term in terms ]
	terms = [term for term in terms if term]
	for ent in ents:
		terms.append(ent)
	additional = addRegexTerms(line)
	for x in additional:
		terms.append(x)
		if DEBUG:
			print( "\t*Added term: " + x) 
	terms = list(set(terms))
	return terms

def addRegexTerms(text):
	additionalTerms = []
	text = text.lower()
	if(DEBUG):
		print("\t*Looking for Regex matches in line: '" + text + "'")
	# Is X a Y?
	m = re.search(r'^is (?P<x>(\w| )+) (a|an) (?P<y>(\w| )+)$', text)
	if (m):
		additionalTerms.append( m.group('x') )
		additionalTerms.append( m.group('y') )
	# How big is X?
	m = re.search(r'how (big|large|tall|small|high)', text)
	if (m):
		additionalTerms.append( 'size' )
		additionalTerms.append( 'length' )
		additionalTerms.append( 'height' )
	# How long is X?
	m = re.search(r'how (long)', text)
	if (m):
		additionalTerms.append( 'length' )
		additionalTerms.append( 'height' )
	# How far is X?
	m = re.search(r'how (far|distant)', text)
	if (m):
		additionalTerms.append( 'distance' )
	# How old is X?
	m = re.search(r'how (old|long ago)', text)
	if (m):
		additionalTerms.append( 'age' )
	# Borders with X?
	m = re.search(r'(borders)|(border)|(next to)|(bordering)', text)
	if (m):
		additionalTerms.append( 'border' )
	# Date of inception of X?
	m = re.search(r'(founded)|(started)|(born)', text)
	if (m):
		additionalTerms.append( 'birth' )
		additionalTerms.append( 'inception' )
	# member of x
	m = re.search(r'(part of)|(member)', text)
	if (m):
		additionalTerms.append( 'member of' )
		additionalTerms.append( 'contains' )
	# highest point of x
	m = re.search(r'(peak)|(highest)', text)
	if (m):
		additionalTerms.append( 'highest point' )
		additionalTerms.append( 'summit' )
	# location
	m = re.search(r'(where)|(location)|(located)', text)
	if (m):
		additionalTerms.append( 'location' )
		additionalTerms.append( 'origin' )
		additionalTerms.append( 'country' )
	if DEBUG:
		print ("\t*Additional groups: " + ", ".join(additionalTerms))
	return additionalTerms

#CONVERT ANY TERM INTO P OR Q VALUES
def convertTerm(term, sort):
	results = []
	if sort == "P":
		params = paramsP
	elif sort == "Q":
		params = paramsQ
	else:
		return ["ERROR"]
	params["search"] = term
	json = requests.get(urlConvert,params).json()
	for result in json['search']:
		results.append("{}".format(result['id']))
	return results

#MAKE QUERY AND RETURN ANSWERS IF ANY
def makeQuery(Q, P):
	answers = []
	query = queryTemplate % (Q, P)
	data = requests.get(urlQuery,params={"query": query, "format": "json"}).json()
	if not data['results']['bindings']:
		return answers
	else:
		for item in data['results']['bindings']:
			for var in item:
				if (var == "answerLabel"):
					answers.append(item[var]["value"])
		return answers

#GENERATE ALL POSSIBLE ANSWERS
def generateAnswers(listP, listQ):
	answers = []
	for Q in listQ:
		for P in listP:
			answers.append(makeQuery(Q, P))
	return answers

#DETERMINE MOST COMMON ANSWER
# This function determines which answer is the most common and returns that,
# if there are ties it results the answer that was found the earliest.
def mostCommonAnswer(answers):
	sortedAnswers = sorted((answer, index) for index, answer in enumerate(answers))
	groups = itertools.groupby(sortedAnswers, key=operator.itemgetter(0))
	def _internal(group):
		item, iterable = group
		count = 0
		minIndex = len(answers)
		for _, where in iterable:
			count += 1
			minIndex = min(minIndex, where)
		return count, -minIndex
	return max(groups, key=_internal)[0]

#SORT
# This sorts the array of Ps or Qs from low to high
# Also removes duplicates
#	i.e. [P123, P231, P4, P4] --> [P4, P123, 231]
def properlySort(givenList, sort):
	newList = []
	givenList = list(set(givenList))
	for each in givenList:
		newList.append(each[1:])
	newList = sorted(newList, key=int)
	if sort == "P":
		newList = ["P" + item for item in newList]
	elif sort == "Q":
		newList = ["Q" + item for item in newList]
	else:
		return ["ERROR"]
	return newList

#MAIN
def main(argv):
	printExamples()
	
	allQuestions = []
	allAnswers = []

	for question in sys.stdin:
		question = re.sub('\d+\s', '', question)
		question = cleanInput(question)
		allQuestions.append(question)

	for question in allQuestions:
		if question:
			#DETERMINE QUESTION TYPE
			questionType = "GENERIC"
			questionList = question.split()
			firstWord = cleanInput(questionList[0].lower())
			if (firstWord == "is" or firstWord == "does" or firstWord == "do"):
				questionType = "YESORNO"
			elif (firstWord == "how" and ("much" in questionList or "many" in questionList)):
				questionType = "QUANTITY"

			#INPUT
			terms = runSpacy(question)
			if DEBUG:
				print("\t*Line: ", question)
				print("\t*Type: ", questionType)
				print("\t*Terms (",  len(terms), "): ", terms, sep="")

			#PROCESS
			# Select one of the terms and convert that into the P
			# and convert all remaining/other terms into Q.
			# Generate all possible answers with those and repeat,
			# until all terms have been converted into P once.
			answers = []
			listP = []
			listQ = []
			for selected in terms:
				listP = convertTerm(selected, 'P')
				listP = properlySort(listP, 'P')
				if listP:
					for other in terms:
						if other is not selected:
							listQ += convertTerm(other, 'Q')
					listQ = properlySort(listQ, 'Q')
				if DEBUG:
					print("\t*Looking for", selected, "properties..")
					print("\t*P (",  len(listP), "/", numberOfUsedP, "): ", listP[:numberOfUsedP], sep="")
					print("\t*Q (",  len(listQ), "/", numberOfUsedQ, "): ", listQ[:numberOfUsedQ], sep="")
				if listQ and listP:
					answers += generateAnswers(listP[:numberOfUsedP], listQ[:numberOfUsedQ])
			answers = [answer for answer in answers if answer]

			#OUTPUT
			if DEBUG:
				print("\t*Answers (",  len(answers), "): ", answers, sep="")
				print("")
			if questionType == "YESORNO":
				# Concatenate all answers into one big list without capitalization or 
				# sublists, check if any of the given terms from the beginning occur in 
				# the found the concatenated answers as well and, if so, answer yes.
				# Not a good solution, but returns yes if the query of some terms 
				# result in the same words that were used in the question itself.
				# e.g. "Is Donald Trump the president of America?"
				if answers:
					termFoundInAnswers = False
					answersConcatenated = []
					for answer in answers:
						answersConcatenated += answer
					answersConcatenated = [answer.lower() for answer in answersConcatenated]
					for term in terms:
						if term in answersConcatenated:
							termFoundInAnswers = True
					if termFoundInAnswers:
						print("yes")
						allAnswers.append("yes")
					else:
						print("no")
						allAnswers.append("no")
				else:
					print("yes")	# Guess if it failed
					allAnswers.append("yes")
			elif questionType == "QUANTITY":
				if answers:
					# Check if the most common answer has the longer answer,
					# otherwise just print the length of the first answer.
					# Stupid solution, but I think it's more likely to be right
					# in these quantity question types.
					if len(answers[0]) > len(mostCommonAnswer(answers)):
						print(len(answers[0]))
						allAnswers.append(len(answers[0]))
					else:
						print(len(mostCommonAnswer(answers)))
						allAnswers.append(len(mostCommonAnswer(answers)))
				else:
					print("no answer found")
					allAnswers.append("")
			elif questionType == "GENERIC":
				if answers:
					# Just the generic answering method, if the most common answer
					# is just one string, print that. If it is a list, print the
					# whole list with tabs in between.
					if isinstance(mostCommonAnswer(answers), list):
						for each in mostCommonAnswer(answers):
							print(each, "\t", sep="", end="")
						print("")
						allAnswers.append(mostCommonAnswer(answers))
					else:
						print(*mostCommonAnswer(answers))
						allAnswers.append(mostCommonAnswer(answers))
				else:
					print("no answer found")
					allAnswers.append("")
			print("")		#newline

	#PRINT TO FILE
	index = 1
	with open("output.txt", "w") as text_file:
		for answer in allAnswers:
			print(index, end="", file=text_file)
			if isinstance(answer, list):
				for subAnswer in answer:
					print("\t", end="", file=text_file)
					print(str(subAnswer), end="", file=text_file)
			else:
				print("\t", end="", file=text_file)
				print(str(answer), end="", file=text_file)
			print(file=text_file)
			index += 1

if __name__ == "__main__":
	main(sys.argv)
