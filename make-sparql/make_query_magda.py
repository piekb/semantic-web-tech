import itertools 
import re

input_folder = "../model/data/"
extra_folder = "../data-rewrite/output/"
output_folder = "result/"
db = "<http://dbpedia.org/"
rdfs = "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"

hardcode_words = {
    "founded by": "founder",
    "film genre": "genre",
    "directed by": "director",
    "movie": "Film",
    "television show": "TelevisionShow",
    "television shows": "TelevisionShow",
    "edited by": "editing"
}

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

f_entities = open(extra_folder + "test-named-entities.txt", "r")
list_entities = f_entities.read().splitlines()

# Open file with encoded queries
f_queries = open(input_folder + "pred-queries.txt", "r")
queries = f_queries.read().splitlines()  # to avoid \n being seen as part of last term

# Open file with correct queries
f_correct_queries = open(extra_folder + "test-correct-sparql.txt", "r", encoding="utf-8")
correct_queries = f_correct_queries.read().splitlines()  # to avoid \n being seen as part of last term

# Files to write something to
f_sparql_queries = open(output_folder + "sparql-queries-magdatest.txt", "a")

def make_terms(l):
    new_l = []
    for entity in l.split("|"):
        ' '.join(entity.split()) # remove double spaces 
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
    #print("Joined list:", "|".join(new_l))
    return new_l
    
queries_noent = []
ents = []

for j, query in enumerate(queries):
    # Make URI terms out of named entities, and compare to correct terms for debugging
    terms = make_terms(list_entities[j].replace(",", "").replace(".", "")) # get rid of all commas and dots
    ents.append(terms)
    new_list = []

    for w in correct_queries[j].split(" "):
        if "http://dbpedia.org/" in w:            
            new_list.append(w.split("/")[-1].split(">")[0])
    # print("Correct entities: ", "|".join(new_list))
    # print(terms)

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
            new_query_list.append(db + "resource/INSERT_ENTITY>")
        elif w == "db_property":
            new_query_list.append(db + "property/INSERT_ENTITY>")
        elif w == "db_ontology":
            new_query_list.append(db + "ontology/INSERT_ENTITY>")
        elif w == "rdf":
            new_query_list.append(rdfs)
        else:
            print(f"[ERROR] Unknown query term:\t{w}")

    # Make sure each new_query_list always ends with a bracket
    if new_query_list[-1] != "}":
        new_query_list.append("}")

    # Join list of strings into one complete string
    new_query = " ".join(new_query_list)
    queries_noent.append(new_query)


# nested loops for substituting the _blank_s for NEs
for query_no in range(len(queries_noent)):
    # if the no. of _blank_s in query is equal to number of NEs
    if len(re.findall("INSERT_ENTITY", queries_noent[query_no])) <= len(ents[query_no]): 
        combinations = list(itertools.permutations(ents[query_no], len(re.findall("INSERT_ENTITY", queries_noent[query_no]))))
        for ne_comb_no in range(len(combinations)):
            comb = combinations[ne_comb_no]  # extract the combination
            subquery = queries_noent[query_no]  # extract the i-th query
            # for every 'INSERT_ENTITY'
            for ne_no in range(len(comb)):
                subquery = re.sub("INSERT_ENTITY", comb[ne_no], subquery, 1)  # substitute I_E for NEs
            f_sparql_queries.write(subquery + "\n")
        f_sparql_queries.write("-" + "\n")   # TODO: some other separator so extraction is easier?
    else:
        f_sparql_queries.write("ERROR: NOT ENOUGH ITEMS \n")
        f_sparql_queries.write("-" + "\n")







    

f_entities.close()
f_queries.close()
f_sparql_queries.close()
f_correct_queries.close()

    


