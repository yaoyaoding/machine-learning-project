#!/usr/bin/python

import sys
import xlearn as xl

action = (["train", "valid"]) [0]

#
#   xlearn_train.py combine.tsv.libffm train.tsv.libffm valid.tsv.libffm test.tsv.libffm 
#
def train() :
#    cf = file(sys.argv[1], "r")
#    ct = file(sys.argv[4], "r")
    model = xl.create_ffm()
    param = {
                'task':'reg', 
                'lr':0.1, 
                'lambda': 1,
                'metric':'rmse',
                'opt':'adagrad',
                'k': 256,
                'stop_window':1,
                'init': 0.1,
                'epoch':4
            }
    model.setTrain(sys.argv[2])
    model.setValidate(sys.argv[3])
    model.setTest(sys.argv[4])
    model.disableNorm();
    model.disableEarlyStop();
    print param
    model.fit(param, "./model.out")
    model.predict("./model.out", "./xprediction.txt")


def valid() :
    print "not implemented"

def main() :
    if action == "train" :
        train()
    else :
        valid()

main()
