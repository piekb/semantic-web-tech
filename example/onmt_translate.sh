#!/bin/bash
python ../OpenNMT-py/onmt/bin/translate.py -model run/model_step_10.pt -src data/src-test.txt -output data/pred_10.txt -verbose
