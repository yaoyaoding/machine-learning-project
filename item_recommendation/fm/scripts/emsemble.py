#!/usr/bin/python

import sys
import os

def trains(src_names, dst_name) :
    print " ".join(src_names)
    print dst_name
    if os.path.exists(dst_name) :
        print dst_name, "has exists"
        exit(0)
    src_files = [ file(fname, "r") for fname in src_names ]
    dst_file = file(dst_name, "w")
    n = len(src_files[0].readlines())
    src_files[0].seek(0)
    head = ""
    for f in src_files:
        head = f.readline()
    dst_file.write(head)

    for i in range(n-1) :
        head = ""
        sums = 0.0
        for f in src_files :
            line = f.readline()
            head = line.split(",")[0]
            sums += float(line.split(",")[1])
        sums /= len(src_files)
        dst_file.write(head + "," + str(sums) + "\n")
    

def main() :
# prog.py a.csv b.csv ... res.csv
    assert len(sys.argv) >= 3
    src_names = sys.argv[1:-1]
    dst_name = (sys.argv[-1:])[0]
    trains(src_names, dst_name)

main()
