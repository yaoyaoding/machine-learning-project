#!/usr/bin/python
#encoding=utf-8
from sklearn.datasets import load_svmlight_file
import xgboost as xgb
import argparse
import datetime
import os
import re

def f(a) :
    a += "a"
    print a

a = "a"
print a
f(a)
print a

# s = [
#         "a",
#         u"你",
#         "8",
#         u"９",
#         u"，"
# 
#         ];
# for a in s :
#     match = re_good.search(a)
#     print match
# 
# #fname = "./expr.svm.txt"
# 
# #train = load_svmlight_file(fname)
