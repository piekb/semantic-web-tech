from SPARQLWrapper import SPARQLWrapper, JSON
import re 
import json

#set the sparql wrapper for dbpedia
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)

#read in the NN-translated queries
queryFile = open('sparql-queries.txt', 'r') 
queries = queryFile.readlines() 
queryFile.close()

outputFile = open("answers.txt","w+")

#take every query and find the answer
for queryNo in range(len(queries)):
    sparqlQuery = queries[queryNo]
    sparqlQuery = re.sub('\\n$', '', sparqlQuery) #remove end of line character
    # TODO: fix queries (e.g. get rid of spaces after underscores)
    print(str(queryNo/len(queries)*100)+'%') # to see some progress
    sparql.setQuery(sparqlQuery)
    results = sparql.query().convert() # find answer
    outputFile.write(str(results)+'\n') # save answer

    
outputFile.close()

