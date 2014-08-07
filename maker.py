#!/usr/bin/python2
#coding:gbk
# maker.py: The Deemo notechart maker. Accepts data from time.txt and write the json notechart.

import json
import os
import sys
def readdata():
	global notesdata,speed,linksdata
	infile=open('time.txt','r')
	rawfiledata=infile.read()[:-1]
	while (a.find('%s\t'%enter)>=0) or (a.find('\t%s'%enter)>=0):
		a=a.replace('%s\t'%enter,enter)
		a=a.replace('\t%s'%enter,enter)
	for i in range(0,len(rawfiledata)):
		while rawfiledata[i].endswith('\t'):rawfiledata[i]=rawfiledata[i][:-1]
	notesdata=rawfiledata[0].split(enter)
	for i in range(0,len(notesdata)):
		while notesdata[i].endswith('\t'):notesdata[i]=notesdata[i][:-1]
	speed=float(rawfiledata[1])
	linksdata=rawfiledata[2].split(enter)
	infile.close()
def parsetone():	#转换音调的字符表达为数字编号，并将d p v三个参数写入sounds列表中的字典
	global sounds
	sounds=[]
	for i in range(0,len(pianotonedata)):
		soundsofanote=[]
		for j in range(0,len(pianotonedata[i])/3):
			tone=pianotonedata[i][3*j+1]
			try:tone=int(tone)	#试图转换为数字
			except:		#如果不是数字
				tonestr=tone
				flag=checktone(tonestr)	#检查是否为合法音符格式
				if not flag:
					print '第',i+1,'行第',j+1,'个音调值有问题，请检查后再运行本程序！'
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
			pianotonedata[i][3*j+1]=int(tone)
			soundsofanote.insert(i,{'d': float(pianotonedata[i][3*j]),'p':pianotonedata[i][3*j+1],'v':int(pianotonedata[i][3*j+2])})
		sounds.insert(i,soundsofanote)

def parsedata():
	global pianotonedata
	for i in range(0,len(notesdata)):notesdata[i]=notesdata[i].split('\t')
	pianotonedata=[]
	for i in range(0,len(notesdata)):
		pianotonedata.insert(i,notesdata[i][3:])
		notesdata[i]=notesdata[i][:3]
	for i in range(0,len(linksdata)):
		while linksdata[i].endswith('\t'):linksdata[i]=linksdata[i][:-1]
		linksdata[i]=linksdata[i].split('\t')
	parsetone()
	
#notesdata[i][j]的结构：
#i为音符编号
#j	数据名称
#0	出现时的秒数
#1	位置[-2,2]
#2	音符大小
#3	钢琴音持续时间
#4	钢琴音音符编号，60为中央C（C4）
#5	钢琴音音量[0,127]
#6	钢琴音持续时间
#7	……
def checktone(tonename):	#检查钢琴音的音调
	if 1<len(tonename)<4:	#长度为2或3
		if (ord(tonename[0].lower()) in range(97,104)) and (ord(tonename[-1]) in range(49,56)):	#第一位为字母且最后一位为1到7数字
			if len(tonename)==3:
				return (tonename[1]=='#' or tonename[1]=='b');#长度为3的，第二位必须为升或降标记
			return True;
	return False;
def checkvolume():	#检查音量值
	for i in range(0,len(pianotonedata)):
		for j in range(0,len(pianotonedata[i])/3):
			try:
				vol=int(pianotonedata[i][3*j+2])
				if not 0<=vol<=127:raise ValueError()
			except:
				print '第',i+1,'行的音量值有问题，请检查后再运行本程序！'
				exit()
def checkpianotone():	#检查钢琴音是否有空白
	checkvolume()
	for i in range(0,len(pianotonedata)):
		for j in range(0,len(pianotonedata[i])/3):
			if not (pianotonedata[i][3*j]=='' and pianotonedata[i][3*j+1]=='' and pianotonedata[i][3*j+2]==''):
				if (pianotonedata[i][3*j]=='' or pianotonedata[i][3*j+1]=='' or pianotonedata[i][3*j+2]==''):
					print '第',i,'行第',j,'个钢琴音有问题，请检查后再运行本程序！'
					exit()

def writejson():
	jsondata={}
	jsondata['speed']=speed	#直接写入速度值
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
	
#主程序开始
if os.name=='nt':enter='\n'
else:enter='\r\n'
#Since this tool deals with Windows text files, it's necessary
#to write this for proper processing in *nix.
readdata()
parsedata()
checkpianotone()
parsetone()
writejson()
