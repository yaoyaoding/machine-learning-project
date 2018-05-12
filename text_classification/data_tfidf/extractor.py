#!/usr/bin/python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import argparse
import os;
import json;
import jieba;
import re;
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.feature_extraction.text import TfidfTransformer 
from sklearn.datasets import dump_svmlight_file

#
#   set the arguments, all is about the input and output files
#
parser = argparse.ArgumentParser(description='transform the json file to svm file(after tfidf transformation)')

parser.add_argument('-ftrain-json', type=str, default='./train.json')
parser.add_argument('-ftest-json', type=str, default='./test.json')
parser.add_argument('-flabel-csv', type=str, default='./train.csv')
parser.add_argument('-ftrain-svm', type=str)
parser.add_argument('-ftest-svm', type=str)

args = parser.parse_args()
args.ftrain_svm = os.path.splitext(args.ftrain_json)[0] + ".3.svm.txt"
args.ftest_svm = os.path.splitext(args.ftest_json)[0] + ".3.svm.txt"

#
#   output arguments for check
#
print "Arguments:\n"
for attr, value in sorted(args.__dict__.items()) :
    print "\t %s = %s" % (attr, value)
check = raw_input("Is that you want?[Y/n]")
if not (check.upper() in ["YES", "Y", ""]) :
    exit()

#
#   read the label csv file and build the label_dict
#
print "Read the label csv file and build the label dictionary...\n"
label_dict = dict()
flabel_csv = file(args.flabel_csv, "r")
for index,line in enumerate(flabel_csv.readlines(), 0) :
    if index == 0 : #   the head
        pass
    identifier, label = line.split(",")
    label_dict[identifier] = label
flabel_csv.close()

#
#   read the train and test json files and build the corpus
#
print "read the train and test json files and build the corpus...\n"
ntrain = 0          #   the first ntrain lines are from train.json, the rest from test.json
corpus = []         #   each entry is a document after cut
train_labels = []   #   the labels of documents in train.json
ftrain_json = file(args.ftrain_json, "r")
ftest_json = file(args.ftest_json, "r")
re_good = re.compile(u'\d|[a-zA-Z]|[\u4e00-\u9fa5]')
for index,f in enumerate([ftrain_json, ftest_json], 0) :
    lines = f.readlines()
    totline = len(lines)
    print "reading the %d file with %d lines..." % (index, totline)
    cur = 0
    for line in lines:
#        if cur == 200000 :
#            break
        if (cur + 1) * 100 / totline != cur * 100 / totline :
            print "\t %d%%" % ((cur + 1) * 100 / totline)
        doc = json.loads(line)
        text = ""
        text += doc[u'content']
        for i in range(20) :
            text += " " + doc[u'title']

        tottext = ""
        for i in range(1,len(text)) :
            if re_good.search(text[i-1]) != None and re_good.search(text[i]) != None:
                tottext += text[i-1] + text[i] + ' '
#        word_list = []
#        for i in range(1,len(text)) :
#            word_list.append(text[i-1] + text[i])
#            print (text[i-1] + text[i])
#        for word in jieba.cut(text, cut_all=False):
#            word_list.append(word)
#        for i in range(1,len(word_list)) :
#            word_list.append(word_list[i-1] + word_list[i])
        corpus.append(tottext)
        if index == 0 :
            ntrain += 1
            train_labels.append(int(label_dict[doc[u'id']]))
        cur += 1
    f.close()

#
#   build the tfidf matrix of the corpus
#
print "build the tfidf matrix of the corpus...\n"
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(corpus)
word = vectorizer.get_feature_names()
transformer = TfidfTransformer()
tfidf = transformer.fit_transform(X)

#
#   output to ftrain_svm and ftest_svm
#
print "output to ftrain_svm and ftest_svm...\n"
test_labels = [ 0 for i in range(tfidf.shape[0]-ntrain) ]
ftrain_svm = file(args.ftrain_svm, "wb")
dump_svmlight_file(tfidf[0:ntrain,:], train_labels, ftrain_svm)
ftrain_svm.close()
ftest_svm = file(args.ftest_svm, "wb")
dump_svmlight_file(tfidf[ntrain:tfidf.shape[0],:], test_labels, ftest_svm)
ftest_svm.close()


