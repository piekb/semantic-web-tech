import ast, re, os

# Settings
blank_word = "_blank_"
input_folder = "input/"
output_folder = "output/"
file_names = ["train-full.txt", "test-full.txt"]

# Create new output folder
os.makedirs(output_folder)

# Do the magic
for n in file_names:
    file = open(input_folder + n, "r")
    file_list = ast.literal_eval(file.read())

    for d in file_list:
        question = d['intermediary_question']
        query = d['sparql_query']

        # Open output files
        base_name = n[:-9]  # returns "train" or "test"
        f_questions = open(output_folder + base_name + "-questions.txt", "a")
        f_named_entities = open(output_folder + base_name + "-named-entities.txt", "a")
        f_queries = open(output_folder + base_name + "-queries.txt", "a")

        # Save named entities and replace them in original questions
        new_question = re.sub("<(.*?)>", blank_word, question)
        named_entities_list = re.findall("<(.*?)>", question)
        named_entities = "|".join(named_entities_list)
        
        # Structure new query based on terms found in original query
        new_query_list = []
        for w in query.split(" "):
            if w == "":
                pass
            elif w == "SELECT":
                new_query_list.append("select")
            elif w == "DISTINCT":
                new_query_list.append("distinct")
            elif w == "WHERE":
                new_query_list.append("where")
            elif w == "ASK":
                new_query_list.append("ask")
            elif w == "?uri":
                new_query_list.append("var_uri")
            elif w == "?x":
                new_query_list.append("var_x")
            elif w == "{":
                new_query_list.append("brack_open")
            elif w == "}":
                new_query_list.append("brack_close")
            elif w == ".":
                new_query_list.append("sep_dot")
            elif w == "COUNT(?uri)":
                new_query_list.append("count_var_uri")
            elif w == "?uri.":
                new_query_list.append("var_uri")
                new_query_list.append("sep_dot")
            elif w == "?uri}":
                new_query_list.append("var_uri")
                new_query_list.append("brack_close")
            elif w == "{?uri":
                new_query_list.append("brack_open")
                new_query_list.append("var_uri")
            elif "resource" in w:
                new_query_list.append("db_resource")
            elif "property" in w:
                new_query_list.append("db_property")
            elif "ontology" in w:
                new_query_list.append("db_ontology")
            elif "rdf" in w:
                new_query_list.append("rdf")
            else:
                print(f"[ERROR] Unknown query term:\t{w}")
        # Make sure each new_query_list always ends with a bracket
        if new_query_list[-1] != "brack_close":
            new_query_list.append("brack_close")
        # Join list of strings into one complete string
        new_query = " ".join(new_query_list)

        # Append results current dict to output files
        f_questions.write(new_question + "\n")
        f_named_entities.write(named_entities + "\n")
        f_queries.write(new_query + "\n")

    f_questions.close()
    f_named_entities.close()
    f_queries.close()
