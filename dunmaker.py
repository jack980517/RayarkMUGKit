#!/usr/bin/env python2
# dunmaker.py: Deemo notechart 'unmaker'. Convert Deemo json notechart to my table notation.
# Usage: dunmaker.py {NOTECHART_FILE_PATH}

import json
import sys
import os
from decimal import *
def readdata(filename):
	global a
	f=open(filename)
	a=json.loads(f.read())
	f.close()
def writedata(filename):
	f=open(filename,'w')
	for i in a['notes']:
		if '_time' not in i:i['_time']=''
		if 'pos' not in i:i['pos']=''
		if 'size' not in i:i['size']=''
		i['_time']=str(i['_time'])
		i['pos']=str(i['pos'])
		i['size']=str(i['size'])
		f.write('%s\t%s\t%s'%(i['_time'],i['pos'],i['size']))
		if 'sounds' in i:
			for cursound in i['sounds']:
				if 'd' not in cursound: cursound['d']=''
				if 'p' not in cursound: cursound['p']=''
				if 'v' not in cursound: cursound['v']=''
				if 'w' not in cursound: cursound['w']=''
				cursound['d']=str(cursound['d'])
				cursound['p']=str(cursound['p'])
				cursound['v']=str(cursound['v'])
				cursound['w']=str(cursound['w'])
				f.write('\t%s\t%s\t%s\t%s'%(cursound['d'],cursound['p'],cursound['v'],cursound['w']))
		f.write(enter)
	f.write('%s%f%s'%(enter,a['speed'],enter))
	for curlink in a['links']:
		f.write(enter)
		tmp=''
		for curnoteinlink in curlink['notes']:
			tmp+=('%s\t'%curnoteinlink['$ref'])
		tmp=tmp[:-1]
		f.write(tmp)
	f.close()
	
infile=[]
outfile=[]
if os.name=='nt':enter='\n'
else:enter='\r\n'
if len(sys.argv)==1:
	infile=['deemo.txt']
	outfile=['deemo_unmake.txt']
for i in range(1,len(sys.argv)):
	for i in range(1,len(sys.argv)):infile.insert(i,sys.argv[i])
	if infile[i-1].rfind('.')==-1:	#If the file is without extension
		for i in range(1,len(sys.argv)):outfile.insert(i,sys.argv[i]+'_unmake.txt')
	else:	#If the file is with extension or path contains "."
		if infile[i-1].rfind('.')>infile[i-1].rfind('\\'):	#If the "." is from file extension
			for i in range(1,len(sys.argv)):outfile.insert(i,sys.argv[i][:sys.argv[i].rfind('.')]+'_unmake.txt')
		else:	#If the "." is from path
			for i in range(1,len(sys.argv)):outfile.insert(i,sys.argv[i]+'_unmake')
	readdata(infile[i-1])
	writedata(outfile[i-1])
