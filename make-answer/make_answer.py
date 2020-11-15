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
answer_indices = indFile.readlines()
indFile.close()

#read in the model-translated queries
queryFile = open('sparql-queries.txt', 'r') 
queries = queryFile.readlines()
queryFile.close()

#read in the test answers
ansFile = open('answers-test.txt', 'r') 
answers_test = ansFile.readlines()
ansFile.close()

outputFile = open("answers.txt","w+")

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
    start_ind = hyphen_indices[int(answerInd)]
    stop_ind = hyphen_indices[int(answerInd)+1]
    answers = []
    
    for queryInd in range(start_ind, stop_ind):
        sparqlQuery = queries[queryInd]
        if sparqlQuery == hyphen:
            outputFile.write("question " + str(answerInd))
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
            
            if is_empty == None:
                answers.append(answer)
            else:
                pass
           
        print(str(round(queryInd/len(queries)*100, 2))+'%')
    outputFile.write('model answer: ' + str(mode(answers)) + '\ntest answer: ' + str(answers_test[int(answerInd)]) + '\n')
    
    if str(mode(answers)) == str(answers_test[int(answerInd)]):
        correct_counter += 1
    else:
        correct_counter += 0

outputFile.write(str(correct_counter/len(answer_indices)) + "%% of answers correct")

    
outputFile.close()
