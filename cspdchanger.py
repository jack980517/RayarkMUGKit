#!/usr/bin/env python2
# cspdchanger.py: Changes the speed of Cytus notecharts.
import json
import os
import sys
from decimal import *	#Use decimal instead of float to ensure precision
def readdata(filename):
	global a
	f=open(filename)
	a=f.read()
	f.close()
	if a.endswith(enter):a=a[:-len(enter)]
	a=a.split(enter)
	
def parseandwrite(filename):
	f=open(filename,'w')
	if a[0]=='VERSION 2':
		print 'VERSION 2 notechart detected'
		parsever2(f)
	elif a[0].startswith('NAME\t'):
		print 'VERSION 1 notechart detected'
		parsever1(f)
	else:
		print 'Not a Cytus notechart!'
		raise IOError()

def parsever1(f):
	print 'Parsing and writing',f.name
	for i in range(0,len(a)):
		a[i]=a[i].split('\t')
		if a[i][0]=='BPM':a[i][1]=str(Decimal(a[i][1])*multiplier)
		if 'SHIFT' in a[i][0]:a[i][1]='%.6f'%(Decimal(a[i][1])/multiplier)
		if a[i][0]=='SECTION':
			a[i][1]='%.6f'%(Decimal(a[i][1])/multiplier)
			a[i][2]='%.6f'%(Decimal(a[i][2])/multiplier)
		if a[i][0]=='NOTE':
			a[i][3]='%.6f'%(Decimal(a[i][3])/multiplier)
			a[i][7]='%.6f'%(Decimal(a[i][7])/multiplier)
		for j in range(0,len(a[i])):
			f.write(a[i][j])
			if j!=len(a[i])-1:f.write('\t')
		f.write('\n')
		
def parsever2(f):
	print 'Parsing and writing',f.name
	for i in range(1,4):a[i]=a[i].split(' ')
	a[1][1]=Decimal(a[1][1])*multiplier
	a[2][1]=Decimal(a[2][1])/multiplier
	a[3][1]=Decimal(a[3][1])/multiplier
	f.write('VERSION 2%sBPM %.6f%sPAGE_SHIFT %.6f%sPAGE_SIZE %.6f%s'%(enter,a[1][1],enter,a[2][1],enter,a[3][1],enter))
	for i in range(4,len(a)):
		if a[i].find('LINK')!=-1:
			notenum=i-5
			break
	for i in range(4,notenum+5):
		a[i]=a[i].split('\t')
		a[i][2]=Decimal(a[i][2])/multiplier
		a[i][4]=Decimal(a[i][4])/multiplier
		f.write('%s\t%s\t%.6f\t%s\t%.6f%s'%(a[i][0],a[i][1],a[i][2],a[i][3],a[i][4],enter))
	for i in range(notenum+5,len(a)):
		f.write('%s%s'%(a[i],enter))
	

#Main program begins
global multiplier
multiplier=Decimal(raw_input('Enter the speed multiplier: '))
infile=[]
outfile=[]
if os.name=='nt':enter='\n'
else:enter='\r\n'
#Since this tool deals with Windows text files, it's necessary
#to write this for proper processing in *nix.
if len(sys.argv)==1:
	infile=['cytus.txt']
	outfile=['cytus_%sx.txt'%multiplier]
for i in range(1,len(sys.argv)):
	for i in range(1,len(sys.argv)):infile.insert(i,sys.argv[i])
	if infile[i-1].rfind('.')==-1:	#If the file is without extension
		for i in range(1,len(sys.argv)):outfile.insert(i,sys.argv[i]+('_%sx'%multiplier))
	else:	#If the file is with extension or path contains "."
		if infile[i-1].rfind('.')>infile[i-1].rfind(os.path.sep):	#If the "." is from file extension
			for i in range(1,len(sys.argv)):outfile.insert(i,sys.argv[i][:sys.argv[i].rfind('.')]+('_%sx.txt'%multiplier))
		else:	#If the "." is from path
			for i in range(1,len(sys.argv)):outfile.insert(i,sys.argv[i]+('_%sx'%multiplier))

	print 'Processing',infile[i-1]
	try:
		readdata(infile[i-1])
		parseandwrite(outfile[i-1])
	except IOError:
		continue
