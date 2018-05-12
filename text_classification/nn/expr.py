#!/usr/bin/python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import random
import os
import numpy as np
from sklearn import metrics
import torch
import datetime
import torch.autograd as autograd
import torch.nn.functional as F
import torch.nn as nn
import torch.utils.data


def auc(predicts, labels) :
    fpr, tpr, thresholds = metrics.roc_curve(labels, predicts, pos_label=1)
    return metrics.auc(fpr, tpr)

print auc(predicts,labels)
#predicts = [ [3, 1], [1, 4], [2, 1], [1, 5] ]
#labels =   [ 1, 0, 1, 0 ]
#print auc(F.softmax(autograd.Variable(torch.Tensor(predicts)),dim=1).data[:,1], labels)
#predicts = autograd.Variable(torch.Tensor(predicts))
#labels = autograd.Variable(torch.LongTensor(labels))
#print F.cross_entropy(predicts, labels)


# pred = autograd.Variable(torch.Tensor([ [1, 3], [3, 1], [0, 1] ]))
# y = autograd.Variable(torch.LongTensor([1, 0, 1]))
# print F.softmax(pred,dim=1)
# print pred
# print y
# loss = F.cross_entropy(pred, y)
# print loss

# inputs = autograd.Variable(torch.Tensor([ 3, 9 ]))
# ooo = F.softmax(inputs, dim=0)
# print ooo
# print ooo[1]
# print ooo[1].data[0]
# 
# 
# inputs = np.ndarray(shape=(5,2))
# for i in range(5) :
#     for j in range(2) :
#         inputs[i][j] = random.uniform(0.0,1.0)
# inputs = autograd.Variable(torch.Tensor(inputs))
# print inputs
# 
# softmax = nn.Softmax(dim = 1)
# loss = nn.CrossEntropyLoss()
# inputs = autograd.Variable(torch.randn(3,2), requires_grad = True)
# targets = autograd.Variable(torch.LongTensor(3).random_(2))
# outputs = loss(inputs, targets)
# print inputs
# print targets
# print outputs
# 
