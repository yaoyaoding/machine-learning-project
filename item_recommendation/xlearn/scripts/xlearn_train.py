#!/usr/bin/python

import os
import sys
import copy
import xlearn as xl

#
#   xlearn_train.py k lambda lr early epoch ftrain fvalid ftest fpred
#
def train(k,lam,lr,early,epoch,train_fname,valid_fname,test_fname,pred_fname) :
    model_fname = "/tmp/model.out"
    param = {
            'task':'reg', 
            'lr':0.1, 
            'lambda': 1, 
            'metric':'rmse',
            'opt':'adagrad',
            'k':60,
            'stop_window':1,
            'epoch':1000,
            }
    param['k'] = k
    param['lambda'] = lam
    param['lr'] = lr
    param['epoch'] = epoch
    
    model = xl.create_ffm()
    model.setTrain(train_fname)
    model.setValidate(valid_fname)
    model.setTest(test_fname)
    model.disableNorm()
    if not early : 
        model.disableEarlyStop()
    model.fit(param, model_fname)
    model.predict(model_fname, pred_fname)

assert len(sys.argv) == 10
train(int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]=="True", int(sys.argv[5]), sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9])



