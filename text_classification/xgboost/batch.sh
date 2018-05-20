#!/bin/bash

./main.py -auto -num-round 1024 -eta 0.05 -subsample 0.6 -max-depth 10
./main.py -auto -num-round 1024 -eta 0.05 -subsample 0.6 -max-depth 12
./main.py -auto -num-round 1024 -eta 0.05 -subsample 0.6 -max-depth 11
./main.py -auto -num-round 1024 -eta 0.05 -subsample 0.6 -max-depth 13

