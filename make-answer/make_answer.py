from SPARQLWrapper import SPARQLWrapper, JSON
import re 
import json
import sys
from statistics import mode

error_msg = 'ERROR: NOT ENOUGH ITEMS \n'
hyphen = '-\n'

#set the sparql wrapper for dbpedia
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)

#read in the indices of functional queries
indFile = open('functional-queries-ind.txt', 'r') 
answer_indices = [int(x) for x in indFile.read().splitlines()]
indFile.close()

#read in the model-translated queries
queryFile = open('sparql-queries.txt', 'r') 
queries = queryFile.readlines()
queryFile.close()

#read in the test answers
ansFile = open('answers-test.txt', 'r') 
answers_test = ansFile.readlines()
ansFile.close()

outputFile = open("answers.txt", "w+")
correctAnswers = open("correct-answers.txt", "w+")

hyphen_indices = []

#find all start- and stop-indices of queries 
for queryNo in range(len(queries)):
    sparqlQuery = queries[queryNo]
    if sparqlQuery == hyphen:
        hyphen_indices.append(queryNo)
    else: 
        pass

correct_counter = 0

#take every query and find the answer
for answerInd in answer_indices:
    start_ind = hyphen_indices[answerInd]
    stop_ind = hyphen_indices[answerInd+1]
    answers = []
    
    for queryInd in range(start_ind, stop_ind):
        sparqlQuery = queries[queryInd]
        if sparqlQuery == hyphen:
            outputFile.write("question " + str(answerInd) + "\n")
            answers.append('')
        elif sparqlQuery == error_msg:
            answers.append('')
        else:
            sparqlQuery = re.sub(' _', '_', sparqlQuery)
            sparqlQuery = re.sub(' >', '>', sparqlQuery)
            sparqlQuery = re.sub('\\n$', '', sparqlQuery).encode('ascii', "ignore") #remove end of line character
            sparql.setQuery(sparqlQuery)
            answer = sparql.query().convert()
            answer = str(str(answer).encode(sys.stdout.encoding, errors='replace'))
            is_empty = re.search("'bindings': [[]]", answer)
            
            if is_empty is None:
                answers.append(answer)
            else:
                pass
           
        print(str(round(queryInd/len(queries)*100, 2))+'%')

    outputFile.write('model answer: ' + str(mode(answers)) + '\ntest answer: ' + str(answers_test[answerInd]) + '\n')

    x = str(mode(answers))
    y = str(answers_test[answerInd])
    z = b"{'head': {'link': []}, 'boolean': False}"

    correct = True
    if x == "":
        correct = False
    else:
        for i, c in enumerate(x):
            if y[i] != c:
                correct = False

    if correct:
        correct_counter += 1
        print("\t Question", answerInd, "is answered correctly.")
        correctAnswers.write("question " + str(answerInd) + "\n")
        correctAnswers.write('model answer: ' + str(mode(answers)) + '\ntest answer: ' + str(answers_test[answerInd]) + '\n')


outputFile.write(str(correct_counter/len(answer_indices)) + "% of answers correct")
print(correct_counter)

outputFile.close()
correctAnswers.close()
