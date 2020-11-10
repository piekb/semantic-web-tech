from SPARQLWrapper import SPARQLWrapper, JSON
import re 
import json

#set the sparql wrapper for dbpedia
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)

#read in the NN-translated queries
queryFile = open('test-correct-sparql.txt', 'r', encoding = 'utf-8') 
queries = queryFile.readlines() 
queryFile.close()

outputFile = open("answers-test.txt","w+")

#take every query and find the answer
for queryNo in range(len(queries)):
    sparqlQuery = queries[queryNo]
    sparqlQuery = re.sub('\\n$', '', sparqlQuery) #remove end of line character
    print(str(queryNo/len(queries)*100)+'%')
    sparql.setQuery(sparqlQuery)
    results = sparql.query().convert()
    outputFile.write(str(results)+'\n').encode('utf8')
    

    
outputFile.close()

