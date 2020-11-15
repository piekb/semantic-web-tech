# Semantic Web Technology: Final Project
By Marieke, Magda and Dirk Jelle

## Running the code
In order to run the code, create an environment based on Python version 3.7.4 and run `pip install -r requirements` in the main directory of this repository. If you want to be able to run the OpenNMT code as well, be sure to run the `install_opennmt.sh` script in order to get that dependency sorted.

## File overview
`data-rewrite` contains two subfolders: input and output. The input folder contains the original dataset. The Python file in there takes these files, applies the pre-processing and spits out data in several files in the output folder.

`model` contains the scripts required to run OpenNMT in order to create the vocabularies, train the model and translate with the model. The data folder contains the pre-processed data which is served as input to the model, and the predictions made by the model. The output folder consists of the model files and logs. There's also a file in there that takes as input the predictions and original test data, in order to calculate the evaluation metrics.

`make-sparql` contains..

`make-answer` contains..

### OpenNMT Documentation
https://opennmt.net/OpenNMT-py/
