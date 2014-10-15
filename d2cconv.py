#!/usr/bin/env python2
# d2cconv.py: Converts Deemo notecharts to Cytus notecharts.
# Usage: d2cconv.py {NOTECHART_FILE_PATH}
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
	bpm='%.6f'%Decimal(raw_input('Provide BPM value for %s: '%filename))
	page_shift='%.6f'%Decimal(raw_input('Provide PAGE_SHIFT value for %s: '%filename))
	page_size='%.6f'%Decimal(raw_input('Provide PAGE_SIZE value for %s: '%filename))
	f=open(filename,'w')
	f.write('VERSION 2%sBPM %s%sPAGE_SHIFT %s%sPAGE_SIZE %s%s'%(enter,bpm,enter,page_shift,enter,page_size,enter))
	newlist=filter(lambda curnote:not((u'pos' in curnote and curnote['pos']>2)or(u'_time' not in curnote)),a['notes'])
	for i in range(0,len(newlist)):
		if (u'pos' not in newlist[i]):newlist[i][u'pos']=0
	for i in range(0,len(newlist)):
		curnote=newlist[i]
		f.write('NOTE\t%d\t%.6f\t%.6f\t%.6f%s'%(i,curnote['_time'],Decimal(curnote['pos'])/Decimal(4)+Decimal(0.5),0,enter))
	for i in range(0,len(a['links'])):
		curlink=a['links'][i]['notes']
		f.write('LINK ')
		for j in range(0,len(curlink)):
			curnoteinlink=curlink[j]
			for k in range(0,len(newlist)):
				curnote=newlist[k]
				if curnote['$id']==curnoteinlink['$ref']:
					f.write('%d '%k)
					break
		f.write(enter)
			

infile=[]
outfile=[]
if os.name=='nt':enter='\n'
else:enter='\r\n'
if len(sys.argv)==1:
	infile=['deemo.txt']
	outfile=['cytus.txt']
for i in range(1,len(sys.argv)):
	for i in range(1,len(sys.argv)):infile.insert(i,sys.argv[i])
	if infile[i-1].rfind('.')==-1:	#If the file is without extension
		for i in range(1,len(sys.argv)):outfile.insert(i,sys.argv[i]+'_cytus')
	else:	#If the file is with extension or path contains "."
		if infile[i-1].rfind('.')>infile[i-1].rfind('\\'):	#If the "." is from file extension
			for i in range(1,len(sys.argv)):outfile.insert(i,sys.argv[i][:sys.argv[i].rfind('.')]+'_cytus.txt')
		else:	#If the "." is from path
			for i in range(1,len(sys.argv)):outfile.insert(i,sys.argv[i]+'_cytus')
	readdata(infile[i-1])
	writedata(outfile[i-1])
