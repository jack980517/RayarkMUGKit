#!/usr/bin/env python2
# dspdchanger.py: Changes the speed of Deemo notecharts.
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
	a=json.loads(a)
	
def parseandwrite(filename):
	f=open(filename,'w')
	print 'Parsing',filename
	for i in range(0,len(a['notes'])):
		a['notes'][i]['_time']=float(Decimal(a['notes'][i]['_time'])/multiplier)
		if a['notes'][i].has_key('sounds'):
			for j in range(0,len(a['notes'][i]['sounds'])):
				if a['notes'][i]['sounds'][j].has_key('d'):
					a['notes'][i]['sounds'][j]['d']=float(Decimal(a['notes'][i]['sounds'][j]['d'])/multiplier)
	print 'Writing',filename
	f.write(json.dumps(a))

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
	infile=['deemo.txt']
	outfile=['deemo_%sx.txt'%multiplier]
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
