#!/usr/bin/python
import xgboost as xgb
import argparse
import datetime
import os

#
#   parse argument
#
#   return args
#
def parse() :
    parser = argparse.ArgumentParser(description = 'use xgboost to do stacking')

#   general arguments
    parser.add_argument('-ftrain-svm', type=str, default='../data_tfidf/train.svm.txt')
    parser.add_argument('-ftest-svm', type=str, default='../data_tfidf/test.svm.txt')
    parser.add_argument('-ftrain-stack', type=str, default='./stack/train.%d.stack')
    parser.add_argument('-ftest-stack', type=str, default='./stack/test.%d.stack')

#   stacking argument
    parser.add_argument('-nflod', type=int, default=3)

#   learning arguments
    parser.add_argument('-num-round', type=int, default=100)
    parser.add_argument('-epoch', type=int, default=10)
    parser.add_argument('-eta', type=float, default=0.05)
    parser.add_argument('-max-depth', type=int, default=13)
    parser.add_argument('-subsample', type=float, default=0.700)    
    parser.add_argument('-colsample-bytree', type=float, default=0.8)
    parser.add_argument('-colsample-bylevel', type=float, default=0.8)
    parser.add_argument('-scale-pos-weight', type=float, default=12.0)
    parser.add_argument('-early-stopping-rounds', type=int, default=10)
    parser.add_argument('-silent', type=int, default=0)
    parser.add_argument('-objective', type=str, default='binary:logistic')
    parser.add_argument('-nthread', type=int, default=4)
    parser.add_argument('-eval-metric', type=str, default='auc')

    args = parser.parse_args()

    for attr, value in sorted(args.__dict__.items()) :
        print "\t %s = %s" % (attr, value)
    return args

#
#   train a model given args and dtrain, dvalid
#
#   return: a booster that has been trained
#   
def train_booster(index, dtrain, dvalid, args) :
    evals = [(dtrain, 'dtrain'), (dvalid, 'dvalid' + str(index))]
    booster = xgb.train(args.__dict__, dtrain, args.num_round * args.epoch, evals,
            early_stopping_rounds=args.early_stopping_rounds)
    return booster

#
#   stack
#   
#   return: train_stack, test_stack
#
def stack(args) :
    print "start stacking..."
    dtrain = xgb.DMatrix(args.ftrain_svm)
    dtest = xgb.DMatrix(args.ftest_svm)
    ntrain = dtrain.num_row()
    ntest = dtest.num_row()
    npart = args.nflod
    part_len = ntrain / npart
    parts = [range(i * part_len, (i+1) * part_len) for i in range(npart-1)]
    parts.append( range((npart-1) * part_len, ntrain) )

    train_stack = [0.0 for i in range(ntrain)]
    test_stack = [0.0 for i in range(ntest)]

    print "there are %d part" % npart
    for i in range(npart) :
        print "[%d,%d] " % (min(parts[i]), max(parts[i])),
    print 
    for i in range(npart) :
        train_rows = []
        valid_rows = []
        for j in range(npart) :
            if j == i :
                valid_rows += parts[j]
            else :
                train_rows += parts[j]
        train = dtrain.slice(train_rows)
        valid = dtrain.slice(valid_rows)
        booster = train_booster(i, train, valid, args)
        valid_result = booster.predict(valid)
        for j in range(len(valid_rows)) :
            train_stack[valid_rows[j]] = valid_result[j]
        test_result = booster.predict(dtest)
        for j in range(ntest) :
            test_stack[j] += test_result[j]
        train = None
        valid = None
    for j in range(ntest) :
        test_stack[j] /= npart
    return train_stack, test_stack

def output_file(data, fname) :
    cur = 0
    while os.path.exists(fname % cur) :
        cur += 1
    fname = fname % cur
    print "write to %s" % fname
    f = file(fname, "w")
    for v in data :
        f.write("%.10f\n" % v)
    f.close()

def main() :
    args = parse()
    train_stack, test_stack = stack(args)
    output_file(train_stack, args.ftrain_stack)
    output_file(test_stack, args.ftest_stack)

main()
