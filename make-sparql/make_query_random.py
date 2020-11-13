import random
import spacy_dbpedia_spotlight

# Settings
input_folder = "../model/data/"
extra_folder = "../data-rewrite/output/"
output_folder = "result/"
db = "<http://dbpedia.org/"
rdfs = "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"

# Dictionary used to reduce number of if-else statements when decoding queries
query_words = {
    "select": "SELECT",
    "distinct": "DISTINCT",
    "where": "WHERE",
    "ask": "ASK",
    "brack_open": "{",
    "brack_close": "}",
    "sep_dot": ".",
    "var_uri": "?uri",
    "var_x": "?x",
    "count_var_uri": "COUNT(?uri)"
}

# TODO: hardcode more words, or find some way to make this dynamic, or ignore and explain bad results
# Dictionary of special URI terms for named entities
hardcode_words = {
    "founded by": "founder",
    "film genre": "genre",
    "directed by": "director",
    "movie": "Film",
    "television show": "TelevisionShow",
    "television shows": "TelevisionShow",
    "edited by": "editing"
}


# TODO: should find the correct term to use (e.g. through brute force, see ../LTP/DirkJelleLTP.py).
# Currently random choice from set of possible entities
def find_entity(uri_terms):
    y = random.choice(uri_terms)
    # print("Random choice:", y)
    return y


# Returns list of named entities, written as correct terms to add to URI's.
# Names: whitespace --> underscore, other terms: whitespace --> camelCase,
# e.g. "river mouth" --> riverMouth, "Stanley Kubrick" --> Stanley_Kubrick.
# Except when the term is between brackets: "John Forbes (British Army officer)"
# --> John_Forbes_(British_Army_officer), NOT John_Forbes(British_ArmyOfficer).
def make_terms(l):
    new_l = []
    for entity in l.split("|"):
        if entity in hardcode_words:
            new_l.append(hardcode_words[entity])
        else:
            skip = False
            bracket = False
            x = ""
            for i, c in enumerate(entity):
                if c == " " and i + 1 < len(entity):
                    if entity[i + 1].isupper() or entity[i + 1] == "(" or bracket:
                        x += "_"
                        if entity[i + 1] == "(":
                            bracket = True
                    else:
                        x += entity[i + 1].capitalize()
                        skip = True
                elif not skip:
                    x += c
                    if c == ")":
                        bracket = False
                else:
                    skip = False
            new_l.append(x)
    # print("Joined list:", "|".join(new_l))
    return new_l


# Open file with encoded queries
f_queries = open(input_folder + "pred-queries.txt", "r")
queries = f_queries.read().splitlines()  # to avoid \n being seen as part of last term

# Open file with correct queries
f_correct_queries = open(extra_folder + "test-correct-sparql.txt", "r")
correct_queries = f_correct_queries.read().splitlines()  # to avoid \n being seen as part of last term

# Open file with full questions to find correct URI's for named entities
f_questions = open("../data-prep/test/test-corrected.txt", "r")
questions = f_questions.read().splitlines()

# Open file with named entities
f_entities = open(extra_folder + "test-named-entities.txt", "r")
list_entities = f_entities.read().splitlines()  # to avoid \n being seen as part of last term

# Files to write something to
f_sparql_queries = open(output_folder + "sparql-queries-random.txt", "a")

for j, query in enumerate(queries):
    # Make URI terms out of named entities, and compare to correct terms for debugging
    terms = make_terms(list_entities[j])
    new_list = []
    list_two = []
    for w in correct_queries[j].split(" "):
        if "http://dbpedia.org/" in w:
            list_two.append(w.split("/")[-2])
            new_list.append(w.split("/")[-1].split(">")[0])
    # print("Correct entities: ", "|".join(new_list))
    # print(" ")
    # print(len(new_list), end="")

    # print(len(terms), end="")
    if len(new_list) > 2:
        # print(questions[j])
        # print(correct_queries[j])
        # print(list_two)
        print(new_list)

    # Structure new query based on terms found in encoded query
    new_query_list = []
    my_list = query.split(" ")
    skipper = False  # to code the reverse of double "new_query_list.append()" lines in data-rewrite.py
    for i, w in enumerate(my_list):
        if w == "" or skipper:
            skipper = False
            pass
        elif w in query_words:
            new_query_list.append(query_words[w])
        elif w == "var_uri" and my_list[i + 1] == "sep_dot":
            new_query_list.append("?uri.")
            skipper = True
        elif w == "var_uri" and my_list[i + 1] == "brack_close":
            new_query_list.append("?uri}")
            skipper = True
        elif w == "brack_open" and my_list[i + 1] == "var_uri":
            new_query_list.append("{?uri")
            skipper = True
        elif w == "db_resource":
            new_query_list.append(db + "resource/" + find_entity(terms) + ">")
        elif w == "db_property":
            new_query_list.append(db + "property/" + find_entity(terms) + ">")
        elif w == "db_ontology":
            new_query_list.append(db + "ontology/" + find_entity(terms) + ">")
        elif w == "rdf":
            new_query_list.append(rdfs)
        else:
            print(f"[ERROR] Unknown query term:\t{w}")

    # Make sure each new_query_list always ends with a bracket
    if new_query_list[-1] != "}":
        new_query_list.append("}")

    # Join list of strings into one complete string
    new_query = " ".join(new_query_list)

    # print("New query:", new_query)
    # print("Correct query:", correct_queries[j])
    # print(" ")
    f_sparql_queries.write(new_query + "\n")

f_entities.close()
f_questions.close()
f_queries.close()
f_sparql_queries.close()
f_correct_queries.close()
