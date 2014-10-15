#!/usr/bin/python2
# pichartgen.py: Generates Deemo notechart for daniwellP's Hatsune Miku 10k digits Pi song.

import json
from decimal import *

f=open('pi.txt','r')
pi=f.read()
f.close()
offset=Decimal('3.110')
secperbeat=Decimal('0.4')
notes=[]
for i in range(0,len(pi)):
	if pi[i]=='.':notes.insert(i,{'$id':str(i+1),'pos':0,'size':1,'_time':float(offset+(i+1)*secperbeat)})
	else:notes.insert(i,{'$id':str(i+1),'pos':float(Decimal('-1.8')+Decimal('0.4')*Decimal(pi[i])),'size':1,'_time':float(offset+(i+1)*secperbeat)})
jsondata={}
jsondata['notes']=notes
jsondata['speed']=10
f=open('pi_deemo.txt','w')
f.write(json.dumps(jsondata))
f.close()
