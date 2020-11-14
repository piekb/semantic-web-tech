from SPARQLWrapper import SPARQLWrapper, JSON
import re 
import json
import sys

error_msg = 'ERROR: NOT ENOUGH ITEMS \n'
hyphen = '-\n'

#set the sparql wrapper for dbpedia
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)

#read in the NN-translated queries
indFile = open('functional-queries-ind.txt', 'r') 
answer_indices = indFile.readlines()
indFile.close()

#read in the NN-translated queries
queryFile = open('sparql-queries.txt', 'r') 
queries = queryFile.readlines()
queryFile.close()

outputFile = open("answers.txt","w+")

hyphen_indices = []

#find all start- and stop-indices of queries 
for queryNo in range(len(queries)):
    sparqlQuery = queries[queryNo]
    if sparqlQuery == hyphen:
        hyphen_indices.append(queryNo)
    else: 
        pass

#take every query and find the answer
for answerInd in answer_indices:
    start_ind = hyphen_indices[int(answerInd)]
    stop_ind = hyphen_indices[int(answerInd)+1]
    for queryInd in range(start_ind, stop_ind):
        sparqlQuery = queries[queryInd]
        if sparqlQuery == hyphen:
            outputFile.write('-\n')
        elif sparqlQuery == error_msg:
            outputFile.write('NO ANSWER DUE TO LACK OF QUERIES\n')
        else:
            sparqlQuery = re.sub(' _', '_', sparqlQuery)
            sparqlQuery = re.sub(' >', '>', sparqlQuery)
            sparqlQuery = re.sub('\\n$', '', sparqlQuery).encode('ascii', "ignore") #remove end of line character
            sparql.setQuery(sparqlQuery)
            answer = sparql.query().convert()
            answer = str(answer).encode(sys.stdout.encoding, errors='replace')
            outputFile.write(str(answer)+'\n')
        print(str(round(queryInd/len(queries)*100, 2))+'%')

    
outputFile.close()
