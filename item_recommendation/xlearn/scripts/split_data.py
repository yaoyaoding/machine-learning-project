#!/usr/bin/python

import sys
import time
import os

#   
#   Given the train and test data, split train into num_part parts.
#   
#   outputs:
#       train0.libfm test0.libfm valid0.libfm
#       ...
#       train(n-1).libfm test(n-1).libfm valid(n-1).libfm
#       points.txt
#
#   usage:
#       split_data.py num_part combine.tsv.libfm test.tsv.libfm parts_dir
#

#   [start,end)
last_progress = -1
def show_progress(cur,start,end) :
    global last_progress
    c = (cur - start + 1) * 100 / (end - start)
    if c == last_progress :
        pass
    else :
        sys.stdout.write("\r[%d%%]" % c)
        sys.stdout.flush()
        if c == 100 :
            last_progress = -1
            sys.stdout.write("\n")
        else :
            last_progress = c

def in_part(points, line, part) :
    if part == 0 :
        return line < points[0]
    else :
        return points[part-1] <= line and line < points[part]

def main() :
    assert len(sys.argv) == 5
    num_part = int(sys.argv[1])
    assert 2 <= num_part and num_part <= 20
    comb_name = sys.argv[2]
    test_name = sys.argv[3]
    parts_dir = sys.argv[4]
    
    comb_file = file(comb_name, "r")
    test_file = file(test_name, "r")

    comb_lines = [line for line in comb_file.readlines()]
    test_lines = [line for line in test_file.readlines()]
    num_comb = len(comb_lines)

    points = [ num_comb * i / num_part for i in range(1,num_part+1)]
    print points
    
    file(os.path.join(parts_dir,"points.txt"), "w").write("\n".join([str(a) for a in points]));

    for part in range(num_part) :
        print "part%d..." % part
        train_out = file(os.path.join(parts_dir, "train" + str(part) + ".libfm"), "w")
        test_out = file(os.path.join(parts_dir, "test" + str(part) + ".libfm"), "w")
        valid_out = file(os.path.join(parts_dir, "valid" + str(part) + ".libfm"), "w")
        for line in test_lines :
            test_out.write(line)
        for i,line in enumerate(comb_lines,0) :
            show_progress(i,0,num_comb)
            if in_part(points, i, part) :
                test_out.write(line)
                valid_out.write(line)
            else :
                train_out.write(line)
        train_out.close()
        test_out.close()


main()
