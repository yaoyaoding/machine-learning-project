#!/usr/bin/python

import os
import sys
import copy
import gc
import xlearn as xl

#
#   Do the stacking
#
#
assert len(sys.argv) == 4
parts_dir = sys.argv[1]
pred_dir = sys.argv[2]
tool_dir = sys.argv[3]
points = [int(s) for s in ("".join(file(os.path.join(parts_dir, "points.txt"), "r").readlines())).split()]
nfold = len(points)

def train(early, param, train_fname, valid_fname, test_fname, pred_fname, log_fname) :

    model_fname = "/tmp/model.out"
    
    all_cmd = "%s %d %f %f %s %d %s %s %s %s" % (
            os.path.join(tool_dir,"xlearn_train.py"), param['k'], param['lambda'], param['lr'], str(early), param['epoch'], train_fname, valid_fname, test_fname, pred_fname)
    os.system(all_cmd)

#    train_cmd = os.path.join(tool_dir, "xlearn_train")
#    predict_cmd = os.path.join(tool_dir, "xlearn_predict")
#    all_cmd = "%s %s -s 5 -p 'adagrad' -x 'rmsd' -v %s -m %s -k %d -r %f -b %f -e %d -nthread 4 -sw 1 --no-norm" % (
#             train_cmd, train_fname, valid_fname, model_fname, param['k'], param['lr'], param['lambda'], param['epoch'])
#    if not early :
#        all_cmd += " --dis-es"
#    print all_cmd
#    os.system(all_cmd)
#    all_cmd = "%s %s %s -o %s -nthread 4" % (
#            predict_cmd, test_fname, model_fname, pred_fname)
#    print all_cmd
#    os.system(all_cmd)

#    model = xl.create_ffm()
#    model.setTrain(train_fname)
#    model.setValidate(valid_fname)
#    model.setTest(test_fname)
#    model.disableNorm()
#    if not early : 
#        model.disableEarlyStop()
#    model.fit(param, model_fname)
#    model.predict(model_fname, pred_fname)
    


def next_tour_index() :
    for i in range(1000) :
        if not os.path.exists(os.path.join(pred_dir,"B%d.pred" % (i))) :
            return i
    return 0

def getlines(fname) :
    f = file(fname, "r")
    lines = [line for line in f.readlines()]
    f.close()
    return lines

def putstr(fname, s) :
    f = file(fname, "w")
    f.write(s)
    f.close()

def tour(early, param) :
    tour_index = next_tour_index()
    print "tour %d..." % tour_index
    putstr(os.path.join(pred_dir, "info%d.txt" % tour_index), str(param))
    A_fname = os.path.join(pred_dir, "A%d.pred" % tour_index)
    B_fname = os.path.join(pred_dir, "B%d.pred" % tour_index)
    Afile = file(A_fname, "w")
    Blist = []
    
    for i in range(nfold) :
        print "part %d..." % i
        train_fname = os.path.join(parts_dir, "train%d.libfm" % ( i))
        valid_fname = os.path.join(parts_dir, "valid%d.libfm" % ( i))
        test_fname = os.path.join(parts_dir, "test%d.libfm" % ( i))
        pred_fname = os.path.join(pred_dir, "AB%d_%d.pred" % (tour_index, i))
        log_fname = os.path.join(pred_dir, "log%d_%d.pred" % (tour_index, i))
        train(early, param, train_fname, valid_fname, test_fname, pred_fname, log_fname)
        lines = getlines(pred_fname)
        num_this_part = 0
        if i == 0 :
            num_this_part = points[0]
        else :
            num_this_part = points[i] - points[i-1]
        num_test = len(lines) - num_this_part
        if i == 0 :
            Blist = [ 0.0 for j in range(num_test)]
        for i,line in enumerate(lines,0) :
            if i < num_test :
                Blist[i] += float(line)
            else :
                Afile.write(line)
    Afile.close()
    Bfile = file(B_fname, "w")
    for s in Blist :
        Bfile.write(str(s / nfold) + "\n")
    Bfile.close()

#
#   stacking.py parts_dir pred_dir xlearn_build_dir
#
def main() :
    param = {
                'task':'reg', 
                'lr':0.1, 
                'lambda': 1.0, 
                'metric':'rmse',
                'opt':'adagrad',
                'k':60,
                'stop_window':1,
                'epoch':1000,
            }
    tour_param = [
#            (False, [('k',200), ('epoch',6)]),
#            (False, [('k',150), ('epoch',8)]),
            (True, [('k',100)]),
            (True, [('k',100), ('lambda', 3)]),
            (True, [('k',100), ('lambda', 0.3)])
            ]
    for early,tparam in tour_param :
        cur_param = copy.deepcopy(param)
        for k,v in tparam :
            cur_param[k] = v
        tour(early,cur_param)

main()

