# coding=utf-8
import re
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.pyplot import cm
import os
from os.path import isfile, join
import subprocess


###################
# To skip n lines #
###################
def skip_lines(n, f):
	for i in range(1,n):
		next(f)
	return next(f)


##########################
# 			MAIN		 #
##########################
if len(sys.argv) < 4:
	print ("python lines.py in out sync")
	exit(1)

fname= sys.argv[1]
out= sys.argv[2]
sync= sys.argv[3]

time= []
sequences= []
lengths= []


with open(fname, 'r+') as f:
	for line in f:
		# Get begining of frame capture
		ltime= re.findall(" (.*) 60480 MHz",line)
		if ltime:
			# Get timestamp
			stime= re.match(r'^00:(.*)', ' '.join(ltime), re.I|re.M)
			tmp= stime.group(1).split(":") 
			insecs= float(tmp[0])*60 + float(tmp[1])
			time.append(insecs)

			# Get tcp seq num
			tmp= re.findall("ack [0-9]*", line)
			if len(tmp) != 0:
				s= tmp[0].split(' ')[1]
				if(int(s)>1000000000):
					s= "0"
				sequences.append(s)
			else:
				sequences.append("0")
f.close()

sequences[0]= "1"
step=1448+1448+1448
#step= int(sequences[0])
#step= int(sequences[1])-int(sequences[0]) 
sequences= [str(int(x) + step  - 1) for x in sequences]
#for i in range(0, len(sequences)):
#	sequences[i]= str(int(sequences[i]) + step  - 1) 

time= [str(float(t) + float(sync)) for t in time]

print( len(time)        )
print( len(sequences)   )  
print( "tcp acks"       )

################################
# 		Writing output		   #
################################


f = open(out, "w")

#f.write(str(time[0])+ "\t")
#f.write(str(sequences[0])+ "\t")
#f.write("0"+ "\t")
#f.write("\n")

for i in range(len(time)):
	f.write(str(time[i])+ "\t")
	f.write(str(sequences[i])+ "\t")
#	f.write(str(float(time[i])-float(time[i-1]))+ "\t")
	f.write("\n")

f.close()




