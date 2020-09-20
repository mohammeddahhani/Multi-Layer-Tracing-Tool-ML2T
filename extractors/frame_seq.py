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
h_offset=0.000686
sync= str(float(sys.argv[3]))

time= []
sequences= []
seq_bit= []


with open(fname, 'r+') as f:
	for line in f:
		# Get timestamp
		ltime= re.findall(" (.*) 60480 MHz",line)
		if ltime:
			stime= re.match(r'^00:(.*)', ' '.join(ltime), re.I|re.M)
			tmp= stime.group(1).split(":") 
			insecs= float(tmp[0])*60 + float(tmp[1])
			time.append(insecs)

			# Get SEQ number
			curr= skip_lines(3, f)
			hexs= curr.split(" ")
			seq= hexs[6]
			byte_1, byte_2 = seq[:int(len(seq)/2)], seq[int(len(seq)/2):]
			seq= "0x"+byte_2+byte_1
			seq_h= hex(int(seq, 16) >> 4) # see wireshark 
			sequences.append(int(seq_h, 16)) 
f.close()

time= [str(float(t) + float(sync)) for t in time]
print( len(time)		)		
print( len(sequences)	)			
print( "mac data frames")



################################
# 		Writing output		   #
################################


f = open(out, "w")

for i in range(len(time)):
	f.write(str(time[i])+ "\t")
	f.write(str(sequences[i])+ "\t")
	f.write("\n")

f.close()




