#import pandas as pd
import argparse
import datetime
import os
import numpy as np
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from sklearn import cross_validation, metrics   #Additional scklearn functions
from sklearn.grid_search import GridSearchCV   #Perforing grid 
from sklearn.datasets import load_svmlight_file

parser = argparse.ArgumentParser(description='use xgboost to train a text classifier and do a predict')
parser.add_argument('-ftrain-svm', type=str, default='../data_tfidf/train.2.svm.txt')
parser.add_argument('-ftest-svm', type=str, default='../data_tfidf/test.2.svm.txt')
args = parser.parse_args()

#dtrain = xgb.DMatrix(args.ftrain_svm)
print "loading data"
#args.ftrain_svm = "./expr.svm.txt"
dtrain = load_svmlight_file(args.ftrain_svm)

param_test1 = {
        'max_depth':[ 6, 9, 12, 15 ],
        'subsample':[ 0.8 ]
        }
gsearch1 = GridSearchCV(
        estimator = XGBClassifier(
            learning_rate = 0.2, 
            n_estimators = 250, 
            max_depth=5,
            min_child_weight=1, 
            gamma=0, 
            subsample=1,
            colsample_bytree=1,
            objective= 'binary:logistic', 
            nthread=4,
            silent=0,
            scale_pos_weight=1
            ), 
        param_grid = param_test1,
        scoring='roc_auc',
        n_jobs=1,
        verbose=True,
        cv=3)
print "fitting"
gsearch1.fit(dtrain[0],dtrain[1])
for item in gsearch1.grid_scores_ :
    print item
print gsearch1.best_params_
print gsearch1.best_score_
