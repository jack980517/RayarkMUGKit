#!/usr/bin/env python2
# push.py: Formats the tab-seperated csv file, and push it to the phone via adb.
import os
song=os.sys.argv[2]
f=open('%s/hard.csv'%os.sys.argv[1])
a=f.read().split('\n')
f.close()
f=open('%s/hard.txt'%os.sys.argv[1],'w')
for i in range(0,len(a)):
	while a[i].endswith('\t'):a[i]=a[i][:-1]
	f.write('%s\n'%a[i])
f.close()
os.system('adb push %s/hard.txt /sdcard/Android/data/com.playstation.psstore/files/psm/npqa00103/application/assets/songs/%s/%s.hard.txt'%(os.sys.argv[1],song,song))
