import os 

for i in range(603000, 604000):
    print i
    cmd = 'python getstockdata.py -c '+ str(i) + ' -s 2014 -e 2016' 
    os.system(cmd)
