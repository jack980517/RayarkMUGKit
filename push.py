#!/usr/bin/env python2
# push.py: Formats the tab-seperated csv file, and push it to the phone via adb.
import os
songname='mandora'
f=open('hard.csv')
a=f.read().split('\n')
f.close()
f=open('hard.txt','w')
for i in range(0,len(a)):
	while a[i].endswith('\t'):a[i]=a[i][:-1]
	f.write('%s\n'%a[i])
f.close()
os.system('adb push ./hard.txt /sdcard/Android/data/com.playstation.psstore/files/psm/npqa00103/application/assets/songs/%s/%s.hard.txt'%(songname,songname))
