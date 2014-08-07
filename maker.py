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
def parsetone():	#ת���������ַ����Ϊ���ֱ�ţ�����d p v��������д��sounds�б��е��ֵ�
	global sounds
	sounds=[]
	for i in range(0,len(pianotonedata)):
		soundsofanote=[]
		for j in range(0,len(pianotonedata[i])/3):
			tone=pianotonedata[i][3*j+1]
			try:tone=int(tone)	#��ͼת��Ϊ����
			except:		#�����������
				tonestr=tone
				flag=checktone(tonestr)	#����Ƿ�Ϊ�Ϸ�������ʽ
				if not flag:
					print '��',i+1,'�е�',j+1,'������ֵ�����⣬����������б�����'
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
	
#notesdata[i][j]�Ľṹ��
#iΪ�������
#j	��������
#0	����ʱ������
#1	λ��[-2,2]
#2	������С
#3	����������ʱ��
#4	������������ţ�60Ϊ����C��C4��
#5	����������[0,127]
#6	����������ʱ��
#7	����
def checktone(tonename):	#��������������
	if 1<len(tonename)<4:	#����Ϊ2��3
		if (ord(tonename[0].lower()) in range(97,104)) and (ord(tonename[-1]) in range(49,56)):	#��һλΪ��ĸ�����һλΪ1��7����
			if len(tonename)==3:
				return (tonename[1]=='#' or tonename[1]=='b');#����Ϊ3�ģ��ڶ�λ����Ϊ���򽵱��
			return True;
	return False;
def checkvolume():	#�������ֵ
	for i in range(0,len(pianotonedata)):
		for j in range(0,len(pianotonedata[i])/3):
			try:
				vol=int(pianotonedata[i][3*j+2])
				if not 0<=vol<=127:raise ValueError()
			except:
				print '��',i+1,'�е�����ֵ�����⣬����������б�����'
				exit()
def checkpianotone():	#���������Ƿ��пհ�
	checkvolume()
	for i in range(0,len(pianotonedata)):
		for j in range(0,len(pianotonedata[i])/3):
			if not (pianotonedata[i][3*j]=='' and pianotonedata[i][3*j+1]=='' and pianotonedata[i][3*j+2]==''):
				if (pianotonedata[i][3*j]=='' or pianotonedata[i][3*j+1]=='' or pianotonedata[i][3*j+2]==''):
					print '��',i,'�е�',j,'�������������⣬����������б�����'
					exit()

def writejson():
	jsondata={}
	jsondata['speed']=speed	#ֱ��д���ٶ�ֵ
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
	
#������ʼ
if os.name=='nt':enter='\n'
else:enter='\r\n'
#Since this tool deals with Windows text files, it's necessary
#to write this for proper processing in *nix.
readdata()
parsedata()
checkpianotone()
parsetone()
writejson()
