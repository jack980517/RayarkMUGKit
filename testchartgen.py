#testchartgen.py: Generates a test Deemo notechart to test the bound of 'pos'.
f=open('testchart.json','w')
f.write('{"speed":7.85,"notes":[{"$id":"')
for i in range(-10,30):
    idandtime=i+11
    pos=i/2.0
    f.write(str(idandtime))
    f.write('","pos":')
    f.write(str(pos))
    f.write(',"size":1,"_time":')
    f.write(str(idandtime))
    f.write('.0,"sounds":[{"p":67,"d":0.5,"v":127}]},{"$id":"')

f.write('41","pos":15,"size":1,"_time":41,"sounds":[{"p":67,"d":0.5,"v":127}]}]}')
