from SPARQLWrapper import SPARQLWrapper, JSON
import re 

#set the sparql wrapper for dbpedia
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)

#read in the NN-translated queries
queryFile = open('sparql-queries.txt', 'r', encoding = 'utf-8') 
queries = queryFile.readlines() 
queryFile.close()

outputFile = open("answers.txt","w+")

#take every query and find the answer
for queryNo in range(100):
    sparqlQuery = queries[queryNo]
    sparqlQuery = re.sub('\\n$', '', sparqlQuery) #remove end of line character
    print(sparqlQuery)
    sparql.setQuery(sparqlQuery)
    results = sparql.query().convert()
    outputFile.write(str(results)+'\n')
    
outputFile.close()

