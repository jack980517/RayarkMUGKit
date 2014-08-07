#!/usr/bin/env python2
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
	f=open(filename)
	f.write()

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
