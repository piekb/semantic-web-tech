#!/bin/bash
python ../OpenNMT-py/onmt/bin/translate.py -model output/model.pt -src data/test-questions.txt -output result/pred.txt -verbose
