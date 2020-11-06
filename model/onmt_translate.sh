#!/bin/bash
python ../OpenNMT-py/onmt/bin/translate.py -model output/model_step_10000.pt -src data/test-questions.txt -output data/pred-queries.txt
