#!/usr/bin/python2
# dmaker.py: The Deemo notechart maker. 
# Usage: dmaker.py {TABLE_FILE_PATH}

import json
import os
import sys
def readdata(filename):
	global notesdata,speed,linksdata
	infile=open(filename,'r')
	rawfiledata=infile.read()[:-1]
	while (rawfiledata.find('%s\t'%enter)>=0) or (rawfiledata.find('\t%s'%enter)>=0):
		rawfiledata=rawfiledata.replace('%s\t'%enter,'%s'%enter)
		rawfiledata=rawfiledata.replace('\t%s'%enter,'%s'%enter)
	rawfiledata=rawfiledata.split('%s%s'%(enter,enter)) #Separate raw file data into 3 parts: NOTES, SPEED, LINKS
	rawfiledata[0]=rawfiledata[0].split('%s'%enter) #Seperate NOTES
	notesdata=rawfiledata[0] #Ready to use
	speed=float(rawfiledata[1])
	linksdata=rawfiledata[2].split('%s'%enter)
	infile.close()
def parsetone():	#Convert character notation of notes into number, and write d, p, v, w to a dict in list 'sounds'
	global sounds
	sounds=[]
	for i in range(0,len(pianotonedata)):
		soundsofanote=[]
		for k in range(0,4-len(pianotonedata[i])%4):
			pianotonedata[i].insert(len(pianotonedata[i]),'')
		for j in range(0,len(pianotonedata[i])/4):
			tone=pianotonedata[i][4*j+1]
			try:tone=int(tone)	#Try to convert to number
			except:		#If it's not a number
				if not tone=='':
					tonestr=tone
					flag=checktone(tonestr)	#Check if it's in valid format
					if not flag:
						print 'Pitch of line',i+1,'sound',j+1,'has problems, check before running this program!'
						exit()
					if tone[0]=='c':offset=0
					if tone[0]=='d':offset=2
					if tone[0]=='e':offset=4
					if tone[0]=='f':offset=5
					if tone[0]=='g':offset=7
					if tone[0]=='a':offset=9
					if tone[0]=='b':offset=11
					tone=(int(tonestr[-1])+1)*12+offset
					if len(tonestr)==3:tone+=1 if tonestr[1]=='#' else -1
			if not tone=='':pianotonedata[i][4*j+1]=int(tone)
			tmp={}
			d,p,v,w=pianotonedata[i][4*j:4*j+4]
			if d!='':tmp['d']=float(d)
			if p!='':tmp['p']=int(p)
			if v!='':tmp['v']=float(v)
			if w!='':tmp['w']=float(w)
			if tmp!={}:soundsofanote.insert(i,tmp)
		sounds.insert(i,soundsofanote)

def parsedata():
	global pianotonedata
	for i in range(0,len(notesdata)):notesdata[i]=notesdata[i].split('\t')
	pianotonedata=[]
	for i in range(0,len(notesdata)):
		pianotonedata.insert(i,notesdata[i][3:])
		notesdata[i]=notesdata[i][:3]
	#pianotonedata normal here
	for i in range(0,len(linksdata)):
		while linksdata[i].endswith('\t'):linksdata[i]=linksdata[i][:-1]
		linksdata[i]=linksdata[i].split('\t')
	checkvolume()
	parsetone()
	
#Structure of notesdata[i][j]
#i is note number
#j	Data
#0	Time
#1	Position[-2,2]
#2	Note size
#3	Piano tone duration
#4	Piano tone pitch
#5	Piano tone volume[0,127]
#6	Piano tone width
#7	...
def checktone(tonename):
	if 1<len(tonename)<4:	#Length is 2 or 3
		if (ord(tonename[0].lower()) in range(97,104)) and (ord(tonename[-1]) in range(49,56)):	#First char is letter and last char is num between 1 to 7
			if len(tonename)==3:
				return (tonename[1]=='#' or tonename[1]=='b');#Those with length 3 must have their 2th char being # or b
			return True;
	return False;
def checkvolume():
	for i in range(0,len(pianotonedata)):
		for j in range(0,len(pianotonedata[i])/4):
			try:
				vol=int(pianotonedata[i][4*j+2])
				if not 0<=vol<=127:raise ValueError()
			except:
				print 'Volume of line',i+1,'sound',j+1,'has problems, check before running this program!'
				exit()

def writejson(filename):
	jsondata={}
	jsondata['speed']=speed	#Directly writes speed
	notes=[]
	for i in range(0,len(notesdata)):
		curnote={}
		#if sounds[i]!=[]:notes.insert(i,{'$id':str(i+1),'sounds':sounds[i],'pos':float(notesdata[i][1]),'size':float(notesdata[i][2]),'_time':float(notesdata[i][0])})
		#else:notes.insert(i,{'$id':str(i+1),'pos':float(notesdata[i][1]),'size':float(notesdata[i][2]),'_time':float(notesdata[i][0])})
		curnote['$id']=str(i+1)
		if notesdata[i][0]!='':curnote['_time']=notesdata[i][0]
		if notesdata[i][1]!='':curnote['pos']=notesdata[i][1]
		if notesdata[i][2]!='':curnote['size']=notesdata[i][2]
		if sounds[i]!='':curnote['sounds']=sounds[i]
		notes.insert(i,curnote)
	jsondata['notes']=notes
	links=[]
	for i in range(0,len(linksdata)):
		notesinlink=[]
		for j in range(0,len(linksdata[i])):
			notesinlink.insert(j,{'$ref':linksdata[i][j]})
		links.insert(i,{'notes':notesinlink})
	if len(linksdata)!=0:jsondata['links']=links
	jsonfile=open(filename,'w')
	jsonfile.write(json.dumps(jsondata))
	jsonfile.close()
	
#Main program starts	
infile=[]
outfile=[]
if os.name=='nt':enter='\n'
else:enter='\r\n'
if len(sys.argv)==1:
	infile=['table.txt']
	outfile=['chart.txt']
for i in range(1,len(sys.argv)):
	for i in range(1,len(sys.argv)):infile.insert(i,sys.argv[i])
	if infile[i-1].rfind('.')==-1:	#If the file is without extension
		for i in range(1,len(sys.argv)):outfile.insert(i,sys.argv[i]+'_chart.txt')
	else:	#If the file is with extension or path contains "."
		if infile[i-1].rfind('.')>infile[i-1].rfind('\\'):	#If the "." is from file extension
			for i in range(1,len(sys.argv)):outfile.insert(i,sys.argv[i][:sys.argv[i].rfind('.')]+'_chart.txt')
		else:	#If the "." is from path
			for i in range(1,len(sys.argv)):outfile.insert(i,sys.argv[i]+'_chart')
	readdata(infile[i-1])
	parsedata()
	writejson(outfile[i-1])
