#!/usr/bin/python
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os;
import json;


fin = file("test_words.json", "r")
text = fin.read()
items = json.loads(text)
for item in items :
    word = item[0]
    count = item[1]
    print "%s %d" % (word, count)

