#!/usr/bin/python
import xgboost as xgb
import argparse
import datetime
import os

parser = argparse.ArgumentParser(description='wrap a txt file into csv file, used by my Kaggle Text Classification task.')
parser.add_argument('fin', type=str, help='the name of first file')
parser.add_argument('-out', type=str, default=None, help='the name of the second file')
parser.add_argument('-label', type=str, default="./wrapper_labels.csv", help="the label file")
args = parser.parse_args()

#
#   read files
#
flabel = file(args.label, "r")
fin = file(args.fin, "r")
lst = []
for index,line in enumerate(flabel.readlines(),0) :
    lst.append(line.replace("\n","").split(","))
for index,line in enumerate(fin.readlines(),0) :
    lst[index+1].append(float(line))
fin.close()
flabel.close()

#
#   write output
#
if args.out == None :
    cur = 0
    while os.path.exists("./c" + str(cur) + ".csv") :
        cur += 1
    args.out = "./c" + str(cur) + ".csv"
print "writing to %s" % args.out
fout = file(args.out, "w")
for a,b in lst :
    fout.write("%s,%s\n" % (a, str(b)))
fout.close()


