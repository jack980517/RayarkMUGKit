#!/usr/bin/env python2
# cuetotext.py: Converts cue file to text with second values.

if os.name=='nt':enter='\n'
else:enter='\r\n'
#Since this tool deals with Windows text files, it's necessary
#to write this for proper processing in *nix.
f=open('time.cue','r')
cue=f.read()
f.close()
cuedata=cue.split('INDEX 01 ')[1:]
for i in range(0,len(cuedata)):cuedata[i]=cuedata[i][:8]
outfile=open('time.txt','w')
for i in cuedata:
	min=int(i.split(':')[0])
	sec=int(i.split(':')[1])
	ltas=int(i.split(':')[2]) #less than a second
	outfile.write(str(min*60+sec+ltas/75.0)+enter) 
        #It's 75-based, not 60-based, so do a little conversion
outfile.close()
