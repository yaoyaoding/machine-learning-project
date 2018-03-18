#!/usr/bin/python

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import json
import jieba
import re
import time

zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')

mdict = dict()

def init_mdict(ffname) :
    ffile = file(ffname, "r")
    lines = ffile.readlines();
    for line in lines :
        (name, fid) = line.split()
        uname = unicode(name)
        mdict[uname] = int(fid)
    ffile.close()

def contain_zh(word) :
    word = word.decode()
    match = zh_pattern.search(word)
    return match != None

start_clock_time = 0

def start_clock() :
    global start_clock_time
    start_clock_time = time.time()

def end_clock() :
    global start_clock_time
    cur_clock_time = time.time()
    print
    print (cur_clock_time - start_clock_time) 

def process(prename) :
    start_clock()
    jsonname = prename + ".json"
    outname = prename + ".zh.if.txt"
    jsonfile = file(jsonname, "r")
    outfile = file(outname, "w")
    print "reading files"
    lines = jsonfile.readlines()
    print "There are total %d articles in %s\n" % (len(lines), jsonname)
    cur = 0
    for line in lines :
        cur = cur + 1
        if(cur % 300 == 0) :
            end_clock()
            print "%d %d%%\n" % (cur, cur * 100 / len(lines))
            start_clock()

#        print "%d loading json..." % cur,
#        start_clock()
        dic = json.loads(line)
        content = (dic[u"content"] + " " + dic[u"title"] + " " + dic[u"title"])
#        end_clock()

#        print "%d jieba cut words..." % cur,
#        start_clock()
        words = jieba.cut(content, cut_all=False)
#        end_clock()
        
#        print "%d outputing..." % cur,
#        start_clock()
#        cstr += dic[u"id"] + " "
        outfile.write(dic[u"id"] + " ")
        for word in words :
            if contain_zh(word) :
                outfile.write(word + " ")
#                cstr += word + " "
        outfile.write("\n")
#        cstr += "\n"
#        end_clock()
    jsonfile.close()
    outfile.close()
#
# start
#


prenames = [ "train" ]

init_mdict("combined_words.txt")
for prename in prenames :
    process(prename)
    
