#!/usr/bin/env python2
# push.py: Formats the tab-seperated csv file, and push it to the phone via adb.
import os
filename=os.sys.argv[1]
song=os.sys.argv[2]
if os.path.exists('%s/%s.hard.csv'%(filename,filename)):
	f=open('%s/%s.hard.csv'%(filename,filename))
	a=f.read().split('\n')
	a=a[:-1]
	f.close()
	f=open('%s/%s.hard.txt'%(filename,filename),'w')
	for i in range(0,len(a)):
		while a[i].endswith('\t'):a[i]=a[i][:-1]
		f.write('%s\n'%a[i])
	f.close()
os.system('adb push %s/%s.hard.txt /sdcard/Android/data/com.playstation.psstore/files/psm/npqa00103/application/assets/songs/%s/%s.hard.txt'%(filename,filename,song,song))
os.system('adb push %s/%s.mp3 /sdcard/Android/data/com.playstation.psstore/files/psm/npqa00103/application/assets/songs/%s/%s.mp3'%(filename,filename,song,song))
os.system('adb push %s/%s_pv.mp3 /sdcard/Android/data/com.playstation.psstore/files/psm/npqa00103/application/assets/songs/%s/%s_pv.mp3'%(filename,filename,song,song))

