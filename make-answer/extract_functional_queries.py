#read in the NN-translated queries
queryFile = open('test-correct-sparql.txt', 'r', encoding='utf-8')
queries = queryFile.readlines() 
queryFile.close()

#read in the answers
answerFile = open('answers-test.txt', 'r', encoding='utf-8')
answers = answerFile.readlines() 
answerFile.close()

#start a new doc to check "correct" answers
outputFile = open('functional-queries-ind.txt', 'w+', encoding='utf-8')

empty_answer = "b\"{'head': {'link': [], 'vars': ['uri']}, 'results': {'distinct': False, 'ordered': True, 'bindings': []}}\"\n"
funct_queries = []

#locate all non-functional queries (by finding empty answer strings)
for line_no in range(len(answers)):
    if answers[line_no] == empty_answer:
        pass
    else:
        funct_queries.append(line_no)
        outputFile.write(str(line_no)+ '\n')


outputFile.close()
