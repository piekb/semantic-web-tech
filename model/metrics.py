# Read files
test_query_file = open('data/test-queries.txt', 'r')
test_queries = test_query_file.readlines()
pred_query_file = open('data/pred-queries.txt', 'r')
pred_queries = pred_query_file.readlines()

# Clean them up and get the structure right
test_queries = [s[:-1].split(" ") for s in test_queries]
pred_queries = [s[:-1].split(" ") for s in pred_queries]
candidates = pred_queries
reference_list = []
for sentence in test_queries:
    reference_list.append([sentence])

# Calculate metrics
from nltk.translate.bleu_score import corpus_bleu
from nltk.translate.nist_score import corpus_nist
bleu_score = round(corpus_bleu(reference_list, candidates), 3)
nist_score = round(corpus_nist(reference_list, candidates), 3)
print(f"BLEU:\t{bleu_score}\nNIST:\t{nist_score}")

# OUTPUT
# BLEU:   0.758
# NIST:   5.627
