#!/usr/bin/python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import numpy
import torch
import datetime
import torch.autograd as autograd
import torch.nn.functional as F
import torch.nn as nn
import torch.utils.data
import word2vec
import model
import train
import mydataset
import argparse

parser = argparse.ArgumentParser(description='hello')
# dataset
parser.add_argument('-datacsv-file', type=str, default='./data/train.csv', help='file path of the csv file')
parser.add_argument('-vecbin-file', type=str, default='./data/comb.vec.100.bin', help='file path of word2vec bin')
parser.add_argument('-zhif-file', type=str, default='./data/train.zh.if.txt', help='file path of zhif file')
parser.add_argument('-valid-zhif-file', type=str, default='./data/valid.zh.if.txt', help='file path of zhif file')
parser.add_argument('-pred-zhif-file', type=str, default='./data/train.zh.if.txt', help='file path of predict zhif file')
parser.add_argument('-pred-outfile', type=str, default='../predictions/c%d.csv', help='file path of predict output file')
parser.add_argument('-model-outfile', type=str, default='./snapshot/%d.model', help='dir to save the snapshots')
# learning
parser.add_argument('-lr', type=float, default=1e-7, help='learning rate')
parser.add_argument('-weight-decay', type=float, default=1e-7, help='weight decay')
parser.add_argument('-epochs', type=int, default=32, help='number of epochs')
parser.add_argument('-batch-size', type=int, default=1, help='batch size')
parser.add_argument('-log-interval', type=int, default=1000, help='log after training the number of batches')
parser.add_argument('-eval-interval', type=int, default=10000, help='eval after training the number of batches')
parser.add_argument('-save-interval', type=int, default=10000, help='save after training the number of batches')
# model
parser.add_argument('-article-length', type=int, default=2048, help='length of the article length')
parser.add_argument('-embed-dim', type=int, default=100, help='number of embedding dimension')  #   old = 32
parser.add_argument('-kernel-num', type=int, default=256, help='number of kernels for each kernel size')
parser.add_argument('-kernel-sizes', type=str, default='2,3,4,5', help='comma-separated kernel size')
# option
parser.add_argument('-snapshot', type=str, default=None, help='the snapshot as the initial state')
parser.add_argument('-train-predict', action='store_true', default=False, help='train and predict')
parser.add_argument('-train', action='store_true', default=False, help='only train')
parser.add_argument('-predict', action='store_true', default=False, help='only predict')

args = parser.parse_args()

def chooseName(s) :
    cur = 0
    while os.path.exists(s % cur) :
        cur += 1
    return s % cur

#   update args
args.kernel_sizes = [int(k) for k in args.kernel_sizes.split(',')]
args.pred_outfile = chooseName(args.pred_outfile)

#   show parameters
print "\nParameters:" 
for attr, value in sorted(args.__dict__.items()):
        print "\t%s=%s" % (attr.upper(), value)

#   model 
cnn = model.Model(args)

#   load initial model
if args.snapshot is not None :
    print "Loading model from %s..." % (args.snapshot)
    cnn.load_state_dict(torch.load(args.snapshot))

if (args.train_predict) or (args.train) :
#   data
    print "loading dataset..."
    dataset = mydataset.MyDataset(args)
    validset = mydataset.MyDataset(args, valid_set=True)

#   train
    print "starting training..."
    train.train(dataset, validset, cnn, args)
    
if (args.train_predict) or (args.predict) :
    print "loading testset..."
    testset = mydataset.MyTestset(args)
    print "predicting..."
    outputs = train.predict(testset, cnn, args)

#
    fout = file(args.pred_outfile, "w")
    for i in outputs :
        fout.write("%.10f\n" % i)
    fout.close()
    exit(0)
#

    flabel = file("../predictions/wrapper_labels.csv", "r")
    fout = file(args.pred_outfile, "w")
    for index,line in enumerate(flabel.readlines(),0) :
        line = line.replace("\n","")
        if index == 0 :
            fout.write("%s\n" % line)
        else :
            fout.write("%s,%.10f\n" % (line, outputs[index-1]))
    flabel.close()
    fout.close()

    print "finished"

