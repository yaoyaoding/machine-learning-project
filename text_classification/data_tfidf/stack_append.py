#!/usr/bin/python
import sys

base = 2500000

stack_pairs = [ 
        ("./stack/test.1.stack", "./stack/train.1.stack"),
        ("./stack/test.2.stack", "./stack/train.2.stack"),
        ("./stack/test.c0.stack", "./stack/train.c0.stack")
    ]
svm_pair = ("test.3.svm.txt", "train.3.svm.txt")
svm_out_pair = ("test.4.svm.txt", "train.4.svm.txt")

svm_lines = [ [], [] ]

print "read svm file..."
for i in range(2) :
    f = file(svm_pair[i],"r")
    lines = f.readlines()
    for line in lines :
        svm_lines[i].append(line.replace("\n",""))
    f.close()

print "read stack files and append features..."
for i in range(len(stack_pairs)) :
    for j in range(2) :
        print "i = ", i, " j = ", j
        f = file(stack_pairs[i][j], "r")
        lines = f.readlines()
        for index,line in enumerate(lines,0) :
            svm_lines[j][index] = svm_lines[j][index] + (" %d:%.10f " % (base+i, float(line)))
        f.close()

print "write back..."
for i in range(2) :
    f = file(svm_out_pair[i], "w")
    for j in range(len(svm_lines[i])) :
        f.write(svm_lines[i][j])
        f.write("\n")
    f.close()



