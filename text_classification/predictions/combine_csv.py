#!/usr/bin/python
import xgboost as xgb
import argparse
import datetime
import os

parser = argparse.ArgumentParser(description='combine two csv files in one, used by my Kaggle Text Classification task.')
parser.add_argument('w', type=float, help='weight of the first part')
parser.add_argument('in1', type=str, help='the name of first file')
parser.add_argument('in2', type=str, help='the name of second file')
parser.add_argument('out', type=str, help='the name of the second file')
args = parser.parse_args()

#
#   read files
#
fin1 = file(args.in1, "r")
fin2 = file(args.in2, "r")
lst = []
for index,line in enumerate(fin1.readlines(),0) :
    lst.append(line.replace("\n","").split(","))
for index,line in enumerate(fin2.readlines(),0) :
    if index == 0 :
        continue
    a = float(lst[index][1])
    b = float(line.split(",")[1])
    lst[index][1] = (a * args.w + b * (1 - args.w));
fin1.close()
fin2.close()

#
#   write output
#
fout = file(args.out, "w")
for a,b in lst :
    fout.write("%s,%s\n" % (a, str(b)))
fout.close()

