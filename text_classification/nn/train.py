#!/usr/bin/python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import torch
import torch.autograd as autograd
from sklearn import metrics
from torch.autograd import Variable
from torch import squeeze
import torch.nn.functional as F
import torch.nn as nn

def outargs(fname,args) :
    f = file(fname, "w")
    for attr, value in sorted(args.__dict__.items()):
        f.write("\t%s=%s\n" % (attr.upper(), value))
    f.close()

def auc(predicts, labels) :
    fpr, tpr, thresholds = metrics.roc_curve(labels, predicts, pos_label=1)
    return metrics.auc(fpr, tpr)

def chooseName(s) :
    cur = 0
    while os.path.exists(s % cur) :
        cur += 1
    return s % cur

def eval_valid(validset, model, args) :
    labels = []
    predicts = []

    model.eval()
    length = len(validset)
#    length = min(length, 500)
    for i in range(length) :
        inputs, label = validset[i]
        inputs = Variable(torch.Tensor(inputs)) #   (W,D)
        inputs = inputs.unsqueeze(0)    #   (1,W,D)
        outputs = model(inputs)         #   (1,C)
        outputs = outputs.squeeze(0)    #   (C)
        p = F.softmax(outputs, dim=0)[1].data[0]
        predicts.append(p)
        labels.append(label)
        if i * 100 / length != (i - 1) * 100 / length :
            sys.stdout.write('\rvalidation [%d%%]' % (i * 100 / length))
            sys.stdout.flush()
    print
    model.train()
    return auc(predicts, labels)

def predict(testset, model, args) :
    y = []
    cur = 0
    total = len(testset)
    print "total %d cases" % total
    model.eval()
    for i in range(len(testset)) :
        cur = cur + 1
        if cur % 2000 == 0 :
            print "cur = %d %d%%" % (cur, cur * 100 / total)
        if(testset[i].shape[0] < 35) :
            y.append(0)
        else :
            inputs = Variable(torch.Tensor(testset[i])) #   (W,D)
            inputs = inputs.unsqueeze(0)    #   (1,W,D)
            outputs = model(inputs)         #   (1,C)
            outputs = outputs.squeeze(0)    #   (C)
            p = F.softmax(outputs, dim=0)[1].data[0]
            y.append(p)
    model.train()
    return y


def train(dataset, validset, model, args) :
    optimizer = torch.optim.SGD(model.parameters(), lr = args.lr, weight_decay = args.weight_decay, momentum=0.9)

    steps = 0

    model.train()
    cur_auc = eval_valid(validset, model, args)
    print('current auc = %.5f' % cur_auc)
    for epoch in range(args.epochs) :
        dataloader = torch.utils.data.DataLoader(dataset, batch_size=args.batch_size, shuffle=True)
        train_iter = iter(dataloader)
        running_loss = 0.0
        print "epoch = %d" % epoch
        psum = [ 0.0, 0.0 ]
        lsum = [ 0, 0 ]
        for batch in train_iter :

            inputs, labels = batch

            inputs = Variable(inputs, requires_grad=True)
            labels = Variable(labels)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = F.cross_entropy(outputs, labels)
            loss.backward()
            optimizer.step()
            logits = F.softmax(outputs, dim=1).data[:,1]
            for j in range(labels.shape[0]) :
                if labels.data[j] == 0 :
                    lsum[0] += 1
                    psum[0] += logits[j]
                else :
                    lsum[1] += 1
                    psum[1] += logits[j]
            
            steps += 1
            running_loss += loss.data[0]

            sys.stdout.write('\r[%4d %3d%%] %.3f %.3f loss:%.3f' 
                    % (100*args.batch_size*(steps) / len(dataset),
                       ((lsum[0] + lsum[1])*100/args.log_interval),
                       (1.0 * psum[0] / (1 + lsum[0])),
                       (1.0 * psum[1] / (1 + lsum[1])),
                       (running_loss / (lsum[0] + lsum[1]))));
            sys.stdout.flush()

            if steps % args.log_interval == 0:
                print
 #               print('0: %.5f' % (1.0 * psum[0] / lsum[0]))
 #               print('1: %.5f' % (1.0 * psum[1] / lsum[1]))
 #               print('[%d, %d * %d %d%%] loss %.3f' % 
 #                   (epoch + 1, steps, len(inputs), 100*args.batch_size*(steps) / len(dataset), running_loss / args.log_interval))
                psum[0] = 0.0
                psum[1] = 0.0
                lsum[0] = 0
                lsum[1] = 0
                running_loss = 0.0
            if steps % args.eval_interval == 0:
                cur_auc = eval_valid(validset, model, args)
                print('current auc = %.5f' % cur_auc)
            if steps % args.save_interval == 0:
                save_path = chooseName(args.model_outfile)
                print "saving %s" % save_path
                torch.save(model.state_dict(), save_path)
                outargs(save_path + ".args",args)


