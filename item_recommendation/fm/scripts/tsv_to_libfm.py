#!/usr/bin/python

#
#   transform the train.tsv, test.tsv, valid.tsv and features.txt to a libfm file
#   
#   tsv_to_libfm.py trans.tsv test.tsv valid.tsv features.txt
#   

import sys
import os

#   data
option = 1  #   0,1,2,3 for libfm format andd 4 for libffm format
comb_entries = []
train_entries = []    #   element:(user,item,score,day,second)
valid_entries = []
test_entries = []
features = []   #   (f1,f2,f3,f4,f5,f6)
user_index = dict()
item_index = dict()
day_index = dict()
second_index = dict()
feature_index = [dict() for i in range(6)]
index_clock = 0

#   read data from file
#   return (features, entries)
def read_tsv(filename, entries) :
    print "reading %s" % filename
    lines = file(filename,"r").readlines() 
    cnt = len(lines)
    for cur,line in enumerate(lines,1):
        if cur * 100 / cnt != (cur - 1) * 100 / cnt :
            sys.stdout.write("\r[%d%%]" % (cur * 100 / cnt))
            sys.stdout.flush()
        entries.append([int(s) for s in line.split()])
    print

def read_features(filename, entries) :
    print "reading %s" % filename
    lines = file(filename,"r").readlines() 
    cnt = len(lines)
    for cur,line in enumerate(lines,1):
        if cur * 100 / cnt != (cur - 1) * 100 / cnt :
            sys.stdout.write("\r[%d%%]" % (cur * 100 / cnt))
            sys.stdout.flush()
        entries.append([int(s) for s in line.split()[1:]])
    print

def add(index_dict, index) :
    global index_clock
    if not index_dict.has_key(index) :
        index_dict[index] = index_clock
        index_clock += 1

def assign_index() :
    print "assigning index..."
    all_entries = [comb_entries, train_entries, valid_entries, test_entries]
    index_dict = [(user_index,0), (item_index,1), (day_index,3), (second_index,4)]
    day_min = 1000000
    day_max = 0
    second_min = 100000000
    second_max = 0
    for entries in all_entries :
        for entry in entries :
            day_min = min(day_min, entry[3])
            day_max = max(day_max, entry[3])
            second_min = min(second_min, entry[4])
            second_max = max(second_max, entry[4])
    for entries in all_entries :
        for entry in entries :
            entry[3] = int((entry[3] - day_min) * 11 / (day_max - day_min)) + 1
            entry[4] = int((entry[4] - second_min) * 23 / (second_max - second_min)) + 1
    for (idict,ii) in index_dict :
        for entries in all_entries :
            for entry in entries :
                add(idict, entry[ii])
    for j in range(6) :
        for feature in features :
            if feature[j] != -1 :
                add(feature_index[j], feature[j])
    print day_min, day_max
    print second_min, second_max
    print day_index
    print second_index

def output_tokens(filename) :
    print "outputing tokens..."
    global index_clock
    lst = [ "" for i in range(index_clock) ]
    for k,v in user_index.iteritems() :
        lst[v] = "user[" + str(k) + "]"
    for k,v in item_index.iteritems() :
        lst[v] = "item[" + str(k) + "]"
    for k,v in day_index.iteritems() :
        lst[v] = "day[" + str(k) + "]"
    for k,v in second_index.iteritems() :
        lst[v] = "second[" + str(k) + "]"
    for i in range(6) :
        for k,v in feature_index[i].iteritems() :
            lst[v] = "feature[" + str(i) + "][" + str(k) + "]"
    f = file(filename, "w")
    for i in range(len(lst)) :
        f.write(str(i) + " " + lst[i] + "\n")
    f.close()
def output_group_meta(filename) :
    print "outputing group meta..."
    global index_clock
    lst = [ -1 for i in range(index_clock) ]
    for k,v in user_index.iteritems() :
        lst[v] = 0
    for k,v in item_index.iteritems() :
        lst[v] = 1
    for k,v in day_index.iteritems() :
        lst[v] = 2
    for k,v in second_index.iteritems() :
        lst[v] = 3
    for i in range(6) :
        for k,v in feature_index[i].iteritems() :
            lst[v] = 4 + i
    f = file(filename, "w")
    for i in range(len(lst)) :
        f.write(str(lst[i]) + "\n")
    f.close()

def output(filename, entries) :
    print "outputing %s" % filename
    f = file(filename, "w")
    cnt_entryes = len(entries)
    for cur_index,entry in enumerate(entries,1) :
        if cur_index * 100 / cnt_entryes != (cur_index - 1) * 100 / cnt_entryes:
            sys.stdout.write("\r[%d%%]" % (cur_index * 100 / cnt_entryes))
            sys.stdout.flush()
        items = []
        user_id, item_id, score, day, second = entry
        items.append((0,user_index[user_id], 1))
        items.append((1,item_index[item_id], 1))
        if option >= 1 :
            items.append((2,day_index[day], 1))
            items.append((3,second_index[second],1))
        if option >= 2 :
            cnt = 0
            for j in range(6) :
                if features[item_id][j] != -1 :
                    cnt += 1
            for j in range(6) :
                if features[item_id][j] != -1 :
                    va = 0.0
                    if option >= 3 :
                        va = 1.0
                    else :
                        va = 1.0 / cnt
                    items.append((4+j,feature_index[j][features[item_id][j]], va))

        items = sorted(items)
        if option <= 3 :
            f.write(str(score) + " " + " ".join([str(index) + ":" + ("%.2f" % value) for field,index,value in items]) + "\n")
        else :
            f.write(str(score) + " " + " ".join([str(field) + ":" + str(index) + ":" + ("%.2f" % value) for field,index,value in items]) + "\n")
    f.close()
    print
    
def main() :
    assert len(sys.argv) == 7
    global option
    global comb_entries
    global train_entries
    global valid_entries
    option = int(sys.argv[1])
#    read_tsv(sys.argv[2], comb_entries)
    read_tsv(sys.argv[3], train_entries)
    read_tsv(sys.argv[4], valid_entries)
    read_tsv(sys.argv[5], test_entries)
    read_features(sys.argv[6], features)
    assign_index()
    output_tokens(os.path.dirname(sys.argv[3]) + "/tokens.txt")
    output_group_meta(os.path.dirname(sys.argv[3]) + "/groups.meta")
#    comb_entries = sorted(comb_entries)
    train_entries = sorted(train_entries)
    valid_entries = sorted(valid_entries)
#    output(sys.argv[2] + ".libfm", comb_entries)
    output(sys.argv[3] + ".libfm", train_entries)
    output(sys.argv[4] + ".libfm", valid_entries)
    output(sys.argv[5] + ".libfm", test_entries)

main()
