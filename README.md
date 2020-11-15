# Semantic Web Technology: Final Project
By Marieke, Magda and Dirk Jelle

## Running the code
In order to run the code, create an environment based on Python version 3.7.4 and run `pip install -r requirements` in the main directory of this repository. If you want to be able to run the OpenNMT code as well, be sure to run the `install_opennmt.sh` script in order to get that dependency sorted.

Scripts should be run separately, in the following order. Please cd to the correct folder, then run the correct file:

1. data-rewrite/data_rewrite.py
2. model/onmt_vocab.sh
3. model/onmt_train.sh
4. model/onmt_translate.sh
5. make-sparql/make_sparql.py
6. make-answer/make_answer_test.py
7. make-answer/extract_functional_queries.py
8. make-answer/make_answer.py

Before running data_rewrite.py, please delete the output folder in the data-rewrite folder, since the script makes it. 

## File overview
`data-rewrite` contains two subfolders: input and output. The input folder contains the original dataset. The Python file in there takes these files, applies the pre-processing and spits out data in several files in the output folder.

`model` contains the scripts required to run OpenNMT in order to create the vocabularies, train the model and translate with the model. The data folder contains the pre-processed data which is served as input to the model, and the predictions made by the model. The output folder consists of the model files and logs. There's also a file in there that takes as input the predictions and original test data, in order to calculate the evaluation metrics.

`make-sparql` contains a folder "result" with the SPARQL queries used for the brute force algorithm in `make-answer`. The file make_query.py is the script to run. It takes as input the lists of entities from data-rewrite/output, and the predicted encoded queries from model/data, and outputs the possible decoded queries to the result folder.

`make-answer` contains: The file "answers.txt" with the numbers of the 484 answerable questions, along with their answers according to the model and what they should be; "correct-answers.txt" shows the same, but only for the 110 correctly answered questions; "answers-test.txt" contains the answers to the test queries; "functional-queries-ind.txt" represents the indices of the functional queries within the test subset; "sparql-queries.txt" and "test-correct-sparql.txt" are input files. Additionally, three scripts are included. "make_answer_test.py" takes in sparql queries from the test set and outputs answers to them; "extract_functional_queries.py" loops over the test answers and extracts the indices of non-empty questions; finally, "make_answer.py" extracts the model-genenrated queries corresponding to the functional questions, retrieves a unique answer and compares the model-generated questions to the desired ones. 

### OpenNMT Documentation
https://opennmt.net/OpenNMT-py/