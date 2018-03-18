#!/usr/bin/python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os;
import json;
import jieba;
import re

zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')

def contain_zh(word) :
    word = word.decode()
    match = zh_pattern.search(word)
    return match != None

jsonfile = file("test.json", "r")
lines = jsonfile.readlines()
print "There are total %d lines\n" % len(lines)
cur = 0
maindict = dict()
totline = len(lines)
for line in lines :
    cur = cur + 1
    if(cur % 1000 == 0) :
        print "%d %d%%\n" % (cur, cur * 100 / totline)
#        break
    dic = json.loads(line)
    content = (dic[u"content"] + " " + dic[u"title"] + " " + dic[u"title"])
#   print content
#   content = content.decode("unicode-escape", "ignore")
    words = jieba.cut(content, cut_all=False)
    for word in words :
        if contain_zh(word) :
            if word in maindict :
                maindict[word] = maindict[word] + 1;
            else :
                maindict[word] = 0
# print maindict
items = sorted(maindict.items(), lambda x, y:cmp(x[1],y[1]), reverse=True)
front = []
for i in xrange(0,min(1000000,len(items))) :
#   print items[i]
    front.append(items[i])
# print front
outfile = file("test_words.txt", "w")
outfile.write(json.dumps(front))
        

