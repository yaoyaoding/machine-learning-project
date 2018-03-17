#!/usr/bin/python
import xgboost as xgb

#
# start
#

# set tran parameters
train_file = './data_ok/train.svm.txt'
# valid_file = 'valid.svm.txt'
test_file = './data_ok/test.svm.txt'
param = dict()
param['max_depth'] = 14
param['max_leaf_nodes'] = 1000
param['eta'] = 0.2
param['silent'] = 1
param['objective'] = 'binary:logistic';
param['nthread'] = 4
param['eval_metric'] = 'auc'
num_round = 150

# read train, valid and test data
dtrain = xgb.DMatrix(train_file)
#dvalid = xgb.DMatrix(valid_file)
dtest = xgb.DMatrix(test_file)
evallist = [(dtrain, 'train')]

# start training
bst = xgb.train(param, dtrain, num_round, evallist)
# bst.save_model('0001.model')
# bst.dump_model('dump.raw.txt')

# start predicting
ypred = bst.predict(dtest)
f = file("ypred.out", "w")
for y in ypred :
    f.write("%f\n" % y)

