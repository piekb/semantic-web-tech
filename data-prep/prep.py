import json
import sys
import nltk


def read_files():
    # reading the data from the file
    with open('train-full.txt') as f:
        data = f.read()

    print("Data type before reconstruction : ", type(data))

    # reconstructing the data as a list of dictionaries
    js = json.loads(data)

    print("Data type after reconstruction : ", type(js))

    # overwriting any existing content to make sure there's no doubles
    f1 = open("sparql.txt", "w", encoding="utf-8")
    f2 = open("intermediary.txt", "w", encoding="utf-8")
    f3 = open("corrected.txt", "w", encoding="utf-8")

    # tokenizing and writing sentences to correct file
    for i, d in enumerate(js):
        s1 = nltk.word_tokenize(d.get('sparql_query'))
        for s in s1:
            f1.write(s + ' ')
        f1.write('\n')

        s2 = nltk.word_tokenize(d.get('intermediary_question'))
        for s in s2:
            f2.write(s + ' ')
        f2.write('\n')

        s3 = nltk.word_tokenize(d.get('corrected_question'))
        for s in s3:
            f3.write(s + ' ')
        f3.write('\n')

    f1.close()
    f2.close()
    f3.close()


# Test...
test = "Which city's foundeer is John Forbes?"
print(nltk.word_tokenize(test))

read_files()