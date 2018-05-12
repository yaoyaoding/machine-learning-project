#!/usr/bin/python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import torch
import torch.autograd as autograd
import torch.nn.functional as F
import torch.nn as nn

class Model(nn.Module) :
    def __init__(self, args) :
        super(Model, self).__init__()
            
        D = args.embed_dim  #   embedding dimension
        C = 2               #   number of categories
        Ci = 1              #   number of input kernels
        Co = args.kernel_num        #   number of output kernels
        Rs = args.kernel_sizes      #   sizes of different regions
        dp = 0.5            #   the ratio of dropout

        self.convs1 = nn.ModuleList([nn.Conv2d(Ci, Co, (R, D)) for R in Rs])
        self.dropout = nn.Dropout(dp)
        self.fc1 = nn.Linear(len(Rs) * Co, C)

    def forward(self, x) :  #   (N, W, D)
        x = x.unsqueeze(1)  #   (N, 1, W, D)
        x = [F.relu(conv(x)).squeeze(3) for conv in self.convs1]     #   [(N, Co, W), ...]*lens(Ks)
        x = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in x]  #   [(N, Co), ...]*lens(Ks)
        x = torch.cat(x, 1)        #   (N, lens(Ks) * Co)
#       x = self.dropout(x) #   (N, lens(Ks) * Co)
        logit = self.fc1(x) #   (N, C)
        return logit

