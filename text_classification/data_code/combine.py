#!/usr/bin/python

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

filenames = [ 'train_words.txt', 'test_words.txt' ]

maindict = dict()
for fn in filenames :
    f = file(fn, 'r')
    lines = f.readlines()
    for line in lines:
        (name,scnt) = line.split()
        cnt = int(scnt)
        if name in maindict :
            maindict[name] += cnt + 1
        else :
            maindict[name] = 0

items = sorted(maindict.items(), lambda x, y:cmp(x[1],y[1]), reverse=True)
fout = file("combined_words.txt", "w")
cout = ""
cur = 0
for (name,cnt) in items :
    if cnt != 0 :
        cout += "%s %d\n" % (name, cur)
        cur += 1
fout.write(cout)

