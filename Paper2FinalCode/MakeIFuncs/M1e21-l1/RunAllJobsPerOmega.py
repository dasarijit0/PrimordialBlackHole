import os
import sys 
import numpy as np

omega = float(sys.argv[1])

direc = 'Omega'+str(omega)+'T/'

mp1 = ["InUpIn.txt","InUpUp.txt","UpInIn.txt","UpInUp.txt","UpUpIn.txt","UpUpUp.txt"]
pp1 = ["InInIn.txt","InInUp.txt","UpInIn.txt","UpInUp.txt","UpUpIn.txt","UpUpUp.txt"]

#os.chdir(direc)

os.chdir(direc+"MinusPlus")
os.system("ls")
for i in range(len(mp1)):
    print(mp1[i])
    os.system("qsub "+str(mp1[i]))

os.chdir("..")
os.chdir("PlusPlus")
for i in range(len(pp1)):
    os.system("qsub "+str(pp1[i]))
   
    
