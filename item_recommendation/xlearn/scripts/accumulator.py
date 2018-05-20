#!/usr/bin/python

import sys
import os

#
#   accumulator.py stack_prediction_dir
#
assert len(sys.argv) == 2

work_dir = sys.argv[1]

train_ans = []
train_features = []
test_features = []

def wjoin(a) :
    return os.path.join(work_dir, a)

def wdjoin(a,b) :
    return os.path.join(work_dir, a, b)

def exist_case(i) :
    aExist = os.path.exists(wjoin("A%d.pred"%i)) 
    bExist = os.path.exists(wjoin("B%d.pred"%i))
    return aExist and bExist


def next_dir() :
    i = 0
    while True :
        print "testing %s" % wdjoin(str(i),"train.libfm")
        if not os.path.exists(wdjoin(str(i),"train.libfm")) :
            return i
        i += 1

def read_features(fname) :
    return [float(s) for s in file(fname,"r").readlines()]

def main() :
    indeces = []
    for i in range(100) :
        if exist_case(i) :
            indeces.append(i)
    if len(indeces) == 0 :
        return
    idir = next_dir()
    os.mkdir(wjoin(str(idir)))
    print "index %d" % idir
    print "valid caces: ", " ".join([str(i) for i in indeces])
    for i in indeces :
        train_features.append(read_features(wjoin("A%d.pred"%i)))
        test_features.append(read_features(wjoin("B%d.pred"%i)))
    train_ans = read_features(wjoin("train_ans.txt"))

    ftrain = file(wdjoin(str(idir),"train.libfm"), "w")
    ftest = file(wdjoin(str(idir),"test.libfm"), "w")
    for i in range(len(train_ans)) :
        ftrain.write(str(train_ans[i]) + " " + " ".join([str(j) + ":" + ("%.3f"%train_features[j][i]) for j in range(len(train_features))]) + "\n")
    for i in range(len(test_features[0])) :
        ftest.write(" ".join([str(j) + ":" + ("%.3f"%test_features[j][i]) for j in range(len(test_features))]) + "\n")

main()



