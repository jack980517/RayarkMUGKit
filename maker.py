#!/usr/bin/python2
# maker.py: The Deemo notechart maker. Accepts data from time.txt and write the json notechart.

import json
import os
import sys
def readdata():
	global notesdata,speed,linksdata
	infile=open('time.csv','r')
	rawfiledata=infile.read()[:-1]
	while (rawfiledata.find('\n\t')>=0) or (rawfiledata.find('\t\n')>=0):
		rawfiledata=rawfiledata.replace('\n\t','\n')
		rawfiledata=rawfiledata.replace('\t\n','\n')
	rawfiledata=rawfiledata.split('\n\n') #Separate raw file data into 3 parts: NOTES, SPEED, LINKS
	rawfiledata[0]=rawfiledata[0].split('\n') #Seperate NOTES
	notesdata=rawfiledata[0] #Ready to use
	speed=float(rawfiledata[1])
	linksdata=rawfiledata[2].split('\n')
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
			if d!='':tmp['d']=d
			if p!='':tmp['p']=p
			if v!='':tmp['v']=v
			if w!='':tmp['w']=w
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

def writejson():
	jsondata={}
	jsondata['speed']=speed	#Directly writes speed
	notes=[]
	for i in range(0,len(notesdata)):
		if sounds[i]!=[]:notes.insert(i,{'$id':str(i+1),'sounds':sounds[i],'pos':float(notesdata[i][1]),'size':float(notesdata[i][2]),'_time':float(notesdata[i][0])})
		else:notes.insert(i,{'$id':str(i+1),'pos':float(notesdata[i][1]),'size':float(notesdata[i][2]),'_time':float(notesdata[i][0])})
	jsondata['notes']=notes
	links=[]
	for i in range(0,len(linksdata)):
		notesinlink=[]
		for j in range(0,len(linksdata[i])):
			notesinlink.insert(j,{'$ref':linksdata[i][j]})
		links.insert(i,{'notes':notesinlink})
	if len(linksdata)!=0:jsondata['links']=links
	jsonfile=open('deemo_chart.txt','w')
	jsonfile.write(json.dumps(jsondata))
	jsonfile.close()
	
#Main program starts
readdata()
parsedata()
writejson()
