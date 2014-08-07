#!/usr/bin/env python2
# c2dconv.py: Converts Cytus notecharts to Deemo notecharts.

import json
import os
import sys
from decimal import *	#Use decimal instead of float to ensure precision
def readdata(filename):
	global a
	f=open(filename)
	a=f.read()
	if a.endswith(enter):a=a[:-len(enter)]
	a=a.split(enter)
	if a[0]!='VERSION 2':
		print 'Not a VERSION 2 Cytus chart, exiting'
		raise IOError()
	f.close()
	
def parsedata():
	global notes,links
	notes=[]
	links=[]
	page_size=Decimal(a[3][10:])
	for i in range(0,len(a)):
		if a[i].find('LINK')!=-1:
			notenum=i-5
			break
	if not a[-1].startswith('LINK'):notenum=len(a)-5
	links=a[notenum+5:]
	for i in range(4,notenum+5):notes.insert(i,a[i].split('\t')[1:])
	for i in range(0,len(notes)):
		for j in range(0,len(notes[i])):
			notes[i][j]=Decimal(notes[i][j])	#Use decimal to ensure precision
	#NOTE	{ID}	{TIME}	{POSITION}	{HOLD_LENGTH}
	for i in range(0,len(notes)):
		notes[i][2]=notes[i][2]*4-2	#Convert Cytus locations [0,1] to Deemo location [-2,2]
		notes[i][3]=notes[i][3]/page_size*Decimal('1.1')+1	#Convert HOLD_LENGTH to size
		#Due to the chart design, page_size is about 11/10 of a bar, so *1.1
	for i in range(0,len(links)):
		links[i]=links[i][:-1]	#Remove ending space
		links[i]=links[i].split(' ')[1:]	#Split & remove the word 'LINK'

def writejson(filename):
	jsondata={}
	notesjson=[]
	linksjson=[]
	for i in range(0,len(notes)):
		notesjson.insert(i,{'$id':str(notes[i][0]+1),'pos':float(notes[i][2]),'size':float(notes[i][3]),'_time':float(notes[i][1])})	#Convert to float at last
	jsondata['notes']=notesjson
	jsondata['speed']=10
	for i in range(0,len(links)):
		notesinlink=[]
		for j in range(0,len(links[i])):
			notesinlink.insert(j,{'$ref':str(int(links[i][j])+1)})
		linksjson.insert(i,{'notes':notesinlink})
	if len(links)!=0:
		jsondata['links']=linksjson
	jsonfile=open(filename,'w')
	jsonfile.write(json.dumps(jsondata))
	jsonfile.close()
	
#Main program begins
infile=[]
outfile=[]
if os.name=='nt':enter='\n'
else:enter='\r\n'
#Since this tool deals with Windows text files, it's necessary
#to write this for proper processing in *nix.
if len(sys.argv)==1:
	infile=['cytus.txt']
	outfile=['deemo.txt']
for i in range(1,len(sys.argv)):
	for i in range(1,len(sys.argv)):infile.insert(i,sys.argv[i])
	if infile[i-1].rfind('.')==-1:	#If the file is without extension
		for i in range(1,len(sys.argv)):outfile.insert(i,sys.argv[i]+'_deemo')
	else:	#If the file is with extension or path contains "."
		if infile[i-1].rfind('.')>infile[i-1].rfind('\\'):	#If the "." is from file extension
			for i in range(1,len(sys.argv)):outfile.insert(i,sys.argv[i][:sys.argv[i].rfind('.')]+'_deemo.txt')
		else:	#If the "." is from path
			for i in range(1,len(sys.argv)):outfile.insert(i,sys.argv[i]+'_deemo')
	try:
		readdata(infile[i-1])
		parsedata()
		writejson(outfile[i-1])
	except:
		continue
