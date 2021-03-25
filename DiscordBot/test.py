import os

turn=0
with open('parameters.csv','r+') as para_file:
    turn=[row.split(sep=',')[1] for row in para_file]
    para_file.seek(0,os.SEEK_SET)
    para_file.write('turn,'+str(int(turn[0])+1))
    para_file.close()