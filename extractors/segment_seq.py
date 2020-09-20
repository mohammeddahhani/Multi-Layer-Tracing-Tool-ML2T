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
sync= str(float(sys.argv[3]))


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

			# Get seg length
			ll= re.findall("length (.*)",line)
			if not ll:
				lengths.append("0")
			else:
				lengths.append(''.join(re.findall("length (.*)",line)))

			# Get tcp seq num
			tmp= ''.join(re.findall("seq (.*):",line))
			if not tmp:
				sequences.append("0")
			else:
				sequences.append(tmp)
	
f.close()

time= [str(float(t) + float(sync)) for t in time]

sequences[0]= "0"
for i in range(len(time)):
	#print time[i] + " seq:"+ sequences[i] + " len:" + lengths[i]
	sequences[i]= str(int(sequences[i]) + int(lengths[i]))


print (len(time)		)
print (len(sequences)	)
print (len(lengths)		)	
print ("tcp segments"	)	


################################
# 		Writing output		   #
################################


f = open(out, "w")


for i in range(len(time)):
	f.write(str(time[i])+ "\t")
	f.write(str(sequences[i])+ "\t")
	f.write("\n")

f.close()
"""

f.write(str(time[0])+ "\t")
f.write(str(sequences[0])+ "\t")
f.write("0"+ "\t")
f.write("\n")

for i in range(1, len(time)):
	f.write(str(time[i])+ "\t")
	f.write(str(sequences[i])+ "\t")
	f.write(str(float(time[i])-float(time[i-1]))+ "\t")
	f.write("\n")

f.close()
"""




