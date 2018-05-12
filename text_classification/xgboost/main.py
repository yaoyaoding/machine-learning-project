#!/usr/bin/python
import xgboost as xgb
import argparse
import datetime
import os

#
#   set the arguments
#
#   general arguments
parser = argparse.ArgumentParser(description='use xgboost to train a text classifier and do a predict')
parser.add_argument('-auto', action='store_true', default=False)
parser.add_argument('-ftrain-svm', type=str, default='../data_tfidf/train.3.svm.txt')
parser.add_argument('-ftest-svm', type=str, default='../data_tfidf/test.3.svm.txt')
parser.add_argument('-ftest-csv', type=str, default='../data_tfidf/test.csv')
parser.add_argument('-fpred-out', type=str, default='../predictions/new%d.csv')
parser.add_argument('-fsave-model', type=str, default='./models/new%d.model')
parser.add_argument('-cv', action='store_true', default=False)
parser.add_argument('-predict-only', action='store_true', default=False)

#   cross validataion arguments
# parser.add_argument('-nfold', type=int, default=4)

#   train arguments
parser.add_argument('-snapshot', type=str, default=None)
parser.add_argument('-num-round', type=int, default=100)
parser.add_argument('-epoch', type=int, default=50)
parser.add_argument('-max-depth', type=int, default=8)
parser.add_argument('-subsample', type=float, default=0.600)    
#parser.add_argument('-early-stopping-rounds', type=int, default=3)
parser.add_argument('-colsample-bytree', type=float, default=0.7)
parser.add_argument('-colsample-bylevel', type=float, default=0.7)
parser.add_argument('-eta', type=float, default=0.01)            #   step size shrinkage used in update to prevents overfitting
#parser.add_argument('-max-leaf-nodes', type=int, default=80)    
parser.add_argument('-scale-pos-weight', type=float, default=12.0)
parser.add_argument('-silent', type=int, default=0)
parser.add_argument('-objective', type=str, default='binary:logistic')
parser.add_argument('-nthread', type=int, default=4)
parser.add_argument('-eval-metric', type=str, default='auc')

args = parser.parse_args()

#
#   output arguments for check
#
print "Arguments:\n"
for attr, value in sorted(args.__dict__.items()) :
    print "\t %s = %s" % (attr, value)
if args.auto == True :
    pass
else :
    check = raw_input("Is that you want?[Y/n]")
    if (not (check.upper() in ["YES", "Y", ""])) :
        exit()

#
#   read the train and test data
#
print "reading data..."
dtrain = xgb.DMatrix(args.ftrain_svm)
dtest = xgb.DMatrix(args.ftest_svm)
evallist = [(dtrain, 'train')]

def predict(bst) :
    print "predict..."
    ypred = bst.predict(dtest)
    cur = 0
    while os.path.exists(args.fpred_out % cur) :
        cur += 1
    ftest_csv = file(args.ftest_csv, "r")
    fpred_out = file(args.fpred_out % cur, "w")
    print "output to ", (args.fpred_out % cur)
    for index,line in enumerate(ftest_csv.readlines(),-1) :
        if index == -1 :    #   head
            fpred_out.write("%s" % line)
        else :
            fpred_out.write("%s,%.10f\n" % (line.split(",")[0], ypred[index]))
    ftest_csv.close()
    fpred_out.close()

#
#   train
#
#bst = xgb.Booster(params=args.__dict__)

if args.predict_only == True :
    if args.snapshot == None :
        exit(0)
    bst = xgb.Booster(model_file=args.snapshot)
    predict(bst)
    exit(0)

if args.snapshot == None :
    last_name = ""
else :
    last_name = args.snapshot

if args.cv :
    for l in range(7,15) :
        args.max_depth = l
        history = xgb.cv(args.__dict__, dtrain, metrics="auc", early_stopping_rounds=20, num_boost_round=args.num_round, verbose_eval=True)
    exit(0)

for epoch in range(args.epoch) :
    print epoch, "train..."
    if last_name == "":
        print "from initial state..."
        bst = xgb.train(args.__dict__, dtrain, args.num_round, evallist)
    else :
        print "load model from ", last_name
        bst = xgb.train(args.__dict__, dtrain, args.num_round, evallist, xgb_model=last_name)

#
#   save model
#
    print "save model..."
    cur = 0
    while os.path.exists(args.fsave_model % cur) :
        cur += 1
    fname = args.fsave_model % cur
    last_name = fname
    bst.save_model(fname)
    print "%s saved." % (fname)

#
#   predict
#
    predict(bst)

