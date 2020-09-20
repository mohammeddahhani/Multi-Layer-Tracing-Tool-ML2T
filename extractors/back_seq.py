# coding=utf-8
import re
import sys
import math
import numpy as np
from math import exp, expm1


def get_last_rcvfr_index(bmap):
	ordered= []
	count1=0
	# Order bits
	for octet in bmap:
		for j in range(len(octet)-1,-1,-1):
			ordered.append(octet[j])
	# Track "1"
	for i in range(len(ordered)):
		if ordered[i] == '1':
			count1= i

	return count1


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
	print ("python back_seq.py in out sync")
	exit(1)

fname= sys.argv[1]
out= sys.argv[2]
sync= sys.argv[3]
h_offset=0.000686
sync= str(float(sys.argv[3]))


time= []
sequences= []
received= []
last_fr_rcvd= []
bitmap= []


with open(fname, 'r+') as f:
	for line in f:
		ltime= re.findall(" (.*) 60480 MHz",line)
		if ltime:
			# Get timestamp
			stime= re.match(r'^00:(.*)', ' '.join(ltime), re.I|re.M)
			tmp= stime.group(1).split(":") 
			insecs= float(tmp[0])*60 + float(tmp[1])
			time.append(insecs)

			# Get SEQ number
			curr= skip_lines(3, f)
			hexs= curr.split(" ")
			seq= hexs[4]
			byte_1, byte_2 = seq[:int(len(seq)/2)], seq[int(len(seq)/2):]
			seq= "0x"+byte_2+byte_1
			seq_h= hex(int(seq, 16) >> 4) # xxxx yyyy looking for xs
			# sequences.append(int(seq_h, 16))
			# Sequence is added later

			# Get BITMAP
			# Split bitmap in bytes 
			bitm= hexs[5:]
			bytelist= [] 
			realbytelist= [] 
			rcvd= 0
			for doctet in bitm:
				h1, h2 = doctet[:int(len(doctet)/2)], doctet[int(len(doctet)/2):]

				if h1.strip() != "00":
					b= bin(int(h1, 16))[2:].zfill(8)
					bb=b
					rcvd+= int(math.log(int(b, 2) + 1, 2))
				else:
					b=0
					bb="00000000"
				bytelist.append(b)
				realbytelist.append(str(bb))

				if h2.strip() !="00":
					b= bin(int(h2, 16))[2:].zfill(8)
					bb=b
					rcvd+= int(math.log(int(b, 2) + 1, 2))					
				else:
					b=0
					bb="00000000"
				bytelist.append(b)
				realbytelist.append(str(bb))

			last_fr_rcvd.append(get_last_rcvfr_index(realbytelist))
			received.append(rcvd) 
			sequences.append(int(seq_h, 16))
			bitmap.append(bytelist)


f.close()

time= [str(float(t) + float(sync)) for t in time]

#for i in range(len(sequences)):
#	sequences[i]= str(int(sequences[i]) \
#					+ int(math.log(int(bitmap[i][0],2)+1, 2)) - 1) 


print (len(time)			)
print (len(sequences)	)	
print (len(received)		)	
print (len(bitmap)		)	
print (len(last_fr_rcvd)	)
#print bitmap

print ("mac block acks")


################################
# 		Writing output		   #
################################


f = open(out, "w")

for i in range(len(time)):
	f.write(str(time[i])+ "\t")
	f.write(str(sequences[i])+ " - " + "\t")
	f.write(str(last_fr_rcvd[i] + sequences[i]) + "\t")
	f.write("(" + str(received[i]) + ")\t")
	f.write(str(''.join(str(bitmap[i]))+ "\t"))
	f.write("\n")

f.close()

#print out + " created"




