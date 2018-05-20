#!/usr/bin/python


import xgboost as xgb
import os
import sys

#
#  ./meta_train.py work_dir
#
assert len(sys.argv)==2
work_dir = sys.argv[1]

def fname(name) :
    return os.path.join(work_dir, name)

def main() :
    dtrain = xgb.DMatrix(fname("train.libfm"))
    dtest = xgb.DMatrix(fname("train.libfm"))
    evallist = [(dtrain, 'train')]

    param = dict()
    param['max_depth'] = 4
    param['eta'] = 0.1
    param['silent'] = 1
    param['objective'] = 'reg:linear'
    param['base_score'] = 50.0
    param['lambda'] = 1.0
    param['gamma'] = 1.0
    param['nthread'] = 4
    param['eval_metric'] = 'rmse'
    param['subsample'] = 0.8

    use_cv = False

    if use_cv :
        xgb.cv(param, dtrain, metrics="rmse", early_stopping_rounds=1, num_boost_round=1000, nfold=3, verbose_eval=True)
    else :
        bst = xgb.train(param, dtrain, num_boost_round=100, evals=evallist)

        ypred = bst.predict(dtest)

        file(fname("prediction.txt"),"w").write("\n".join(["%.7f"%s for s in ypred]))

main()

