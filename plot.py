import plotly.plotly as py
import plotly.tools as tls
import numpy as np

import matplotlib.pyplot as plt; plt.rcdefaults()

import sys


"""
Needs to be changed

Only handles a special case
"""
def moduloToLinear(fr):
	zero=False
	for i in range(len(fr)):
		if(fr[i]==0):
			zero=True
		if(zero):
			fr[i]+=1077
	return fr


"""
Fix issue related to convertion from binary to string 

Captured trace in capture.pcap showed some errors when translated to
string format (.str file in the ./tcp_sender and ./tcp_receiver folders)
"""
def fixAckSeq(tt, ack): 
	for i in range(len(tt)):
		if(tt[i]>=19):
			ack[i]+=1448	
	return ack

t1= []
t2= []
t3= []
t4= []
seg= []
ack= []
frame= []
back= []


##############
#			 #
#  GET FILE  #
#			 #
##############

if len(sys.argv) < 4:
	print ("python plot.py 'seg' 'ack' 'frame' 'back' ")
	exit(1)

tcp_seg= sys.argv[1]
tcp_ack= sys.argv[2]
mac_fr= sys.argv[3]
mac_back= sys.argv[4]



################
#			   #
# EXTRACT DATA #
#              #
################

f=open(tcp_seg,"r")
lines=f.readlines()
f.close()
print(tcp_seg)
for l in lines:
	if(float(l.split('\t')[1]) <= 1):
		lines.remove(l)
for line in lines:
	t1.append(float(line.split('\t')[0]))
	seg.append(float(line.split('\t')[1]))


f=open(tcp_ack,"r")
lines=f.readlines()
f.close()
for line in lines:
	t2.append(float(line.split('\t')[0]))
	ack.append(float(line.split('\t')[1]))


f=open(mac_fr,"r")
lines=f.readlines()
f.close()
for line in lines:
	t3.append(float(line.split('\t')[0]))
	frame.append(float(line.split('\t')[1]))

f=open(mac_back,"r")
lines=f.readlines()
f.close()
for line in lines:
	t4.append(float(line.split('\t')[0]))
	tmp=line.split('\t')[1]
	tmp=tmp.split('-')
	back.append(float(tmp[0]))



############################
#						   #
# PLOT TIME SEQUENCE GRAPH #
#						   #
############################

fig= plt.figure(1)
plt.grid(False)

t1 = np.array(t1) # time dimension according to TCP segments
t2 = np.array(t2) # time dimension according to TCP acks
t3 = np.array(t3) # time dimension according to MAC frames
t4 = np.array(t4) # time dimension according to MAC block acks

seg= np.array(seg)
ack= np.array(ack)
back= np.array(back)
frame= np.array(frame)	

frame=moduloToLinear(frame)
back=moduloToLinear(back)

ack=fixAckSeq(t2, ack)


# upper limit on the range of time axis (x-axis)
off=200 


###################################################################
# IMPORTANT: 													  #
#																  #
# The 3 variables below must modified in order to shift MAC       #
# sequence space to the right region relative to the TCP sequence #
# space                                                           #
#                                                                 #
###################################################################

tcp_shift = 205000
mac_shift = 300000
mac_scale = 500

plt.plot(t1[t1<off], 	 seg[t1<off]+ tcp_shift , 'bD', label="TcpData")
plt.plot(t2[t2<off], 	 ack[t2<off]+ tcp_shift , 'ro', label="TcpAck")	
plt.plot(t3[t3<off], mac_scale*frame[t3<off]-mac_shift, 'kD', label="MacData")
plt.plot(t4[t4<off], mac_scale*back [t4<off]-mac_shift, 'yo', label="MacBack")



plt.ylabel('Sequence Space')
plt.xlabel('Time[s]')
#plt.title('MAC layer time/sequence plot\n AP -> STA')

plt.legend(loc='upper left')
plt.show()




