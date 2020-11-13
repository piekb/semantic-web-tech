# Standard script to compare two text files and write the lines that differ in a new file.
with open('result/sparql-queries-magdatest.txt', 'r') as file1:
    with open('result/sparql-queries-bf.txt', 'r') as file2:
        same = set(file1).difference(file2)

same.discard('\n')

with open('result/comparison.txt', 'a') as file_out:
    for line in same:
        file_out.write(line)