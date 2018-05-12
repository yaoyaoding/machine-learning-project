#!/usr/bin/python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import numpy
import torch
import torch.autograd as autograd
import torch.nn.functional as F
import torch.nn as nn
import torch.utils.data
import word2vec
import model
import train
import argparse

class MyDataset(torch.utils.data.Dataset) :
    def __init__(self,args,valid_set=False) :
        self.idict = dict()
        self.lines = []
        self.model = word2vec.load(args.vecbin_file)
        self.args = args
        
        for line in file(args.datacsv_file,"r").readlines() :
            if(len(line) > 50) :
                iid, label = line.split(",")
                self.idict[iid] = label

        if valid_set :
            lines = file(args.valid_zhif_file, "r").readlines()
        else :
            lines = file(args.zhif_file, "r").readlines()
        for line in lines :
            if line.count(' ') < 35 :
                continue
            self.lines.append(line)
        print "read %d valid lines" % len(self.lines)

    def __len__(self) :
        return len(self.lines)

    def __getitem__(self, idx) :
        line = self.lines[idx]
        items = line.split()
        label = int(self.idict[items[0]])
        valid_cnt = 0
        for word in items[1:] :
            if unicode(word) in self.model :
                valid_cnt += 1
        length = valid_cnt
        length = max(length, 100)
        lrect = numpy.ndarray(shape=(length,self.args.embed_dim), dtype='float32')
        cur = 0
        for word in items[1:] :
            if unicode(word) in self.model :
                if cur < lrect.shape[0]:
                    vec = self.model[unicode(word)]
                    assert(vec.shape[0] == lrect.shape[1])
                    for j in range(0,self.args.embed_dim) :
                        lrect[cur][j] = vec[j]
                    cur += 1
                else :
                    break
        for cur in range(cur,lrect.shape[0]) :
            for k in range(self.args.embed_dim) :
                lrect[cur][k] = 0.0;
        return [lrect, label]

class MyTestset(torch.utils.data.Dataset) :
    def __init__(self,args) :
        self.lines = []
        self.model = word2vec.load(args.vecbin_file)
        self.args = args
        
        lines = file(args.pred_zhif_file, "r").readlines()
        for line in lines :
            self.lines.append(line)

    def __len__(self) :
        return len(self.lines)

    def __getitem__(self, idx) :
        line = self.lines[idx]
        items = line.split()
        valid_cnt = 0
        for word in items[1:] :
            if unicode(word) in self.model :
                valid_cnt += 1
        valid_cnt = valid_cnt
        lrect = numpy.ndarray(shape=(valid_cnt,self.args.embed_dim), dtype='float32')
        cur = 0
        for word in items[1:] :
            if unicode(word) in self.model :
                if cur < lrect.shape[0] :
                    vec = self.model[unicode(word)]
                    for j in range(0,self.args.embed_dim) :
                        lrect[cur][j] = vec[j]
                    cur += 1
                else :
                    break
        for j in range(cur, lrect.shape[0]) :
            for k in range(self.args.embed_dim) :
                lrect[j][k] = 0.0;
        return lrect

