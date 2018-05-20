#!/usr/bin/python

import sys
import os

#
#   transform the prediction file like
#   33.5
#   59.6
#   88.1
#   ...
#   to csv file that contains information of user id and item id like
#   0#11,33.5
#   1#42,59.6
#   33#44,88.1
#   ...
#

def trans(testname, predname, outname) :
    test_lines = [line for line in file(testname,"r").readlines()]
    pred_lines = [line for line in file(predname,"r").readlines()]
    out_lines = ["uid#iid,pred\n"]
    assert len(test_lines) == len(pred_lines)
    n = len(test_lines)
    for i in range(n) :
        items = test_lines[i].split("\t")
        out_lines.append(str(items[0]) + "#" + str(items[1]) + "," + str(max(0.0,min(100.0,float(pred_lines[i])))) + "\n")
    outfile = file(outname, "w")
    outfile.write("".join(out_lines))
    outfile.close()

def main() :
    assert len(sys.argv) == 4
    trans(sys.argv[1], sys.argv[2], sys.argv[3])

main()




