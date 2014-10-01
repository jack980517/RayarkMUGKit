#!/usr/bin/env python2
# push.py: Push the mp3 file to the phone via adb.
import os
song=os.sys.argv[2]
os.system('adb push %s/%s.mp3 /sdcard/Android/data/com.playstation.psstore/files/psm/npqa00103/application/assets/songs/%s/%s.mp3'%(os.sys.argv[1],os.sys.argv[1],song,song))
os.system('adb push %s/%s_pv.mp3 /sdcard/Android/data/com.playstation.psstore/files/psm/npqa00103/application/assets/songs/%s/%s_pv.mp3'%(os.sys.argv[1],os.sys.argv[1],song,song))

