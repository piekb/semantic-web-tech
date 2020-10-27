import json
import sys
import nltk


def file_path(arg, s):
    return arg + '/' + arg + '-' + s + '.txt'


# write each sentence to the correct file, space between each token
def write_to(file, tokenized_sentence):
    # word_tokenize doesn't tokenize possessive apostrophe
    for token in tokenized_sentence:
        if token == "'s":
            file.write("' s ")
        else:
            file.write(token + ' ')
    file.write('\n')


# arg is test or train
def read_files(arg):
    # reading the data from the file
    with open(file_path(arg, 'full')) as f:
        data = f.read()

    # reconstructing the data as a list of dictionaries
    js = json.loads(data)

    # overwriting any existing content to make sure there's no doubles
    f1 = open(file_path(arg, 'sparql'), "w", encoding="utf-8")
    f2 = open(file_path(arg, 'intermediary'), "w", encoding="utf-8")
    f3 = open(file_path(arg, 'corrected'), "w", encoding="utf-8")

    # tokenizing and writing sentences to correct file
    for i, d in enumerate(js):
        write_to(f1, nltk.word_tokenize(d.get('sparql_query')))
        write_to(f2, nltk.word_tokenize(d.get('intermediary_question')))
        write_to(f3, nltk.word_tokenize(d.get('corrected_question')))

    f1.close()
    f2.close()
    f3.close()


# Test...
test = nltk.word_tokenize("Which city's foundeer is John Forbes?")
print(test)
for s in test:
    if s == "'s":
        print("' s ", end=' ')
    else:
        print(s + ' ', end=' ')
print('')

read_files(sys.argv[1])
