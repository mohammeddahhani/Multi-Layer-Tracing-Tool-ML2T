#!/bin/sh

if [ "$#" -ne 1 ]; then
    echo "Which .pcap to use ? \nUsage: ./extract capture.pcap"
    exit 1
fi

# Sender & receiver IP and MAC addresses : TO ADAPT !!!

#####################
sndmac=0x0a9c		# Last two octet of TCP sender MAC address e.g. 11:22:33:44:xx:yy
rcvmac=0x0b7e		# Last two octet of TCP receiver MAC address e.g. 11:22:33:44:xx:yy
sndip=0x01			# Last octet of the TCP sender's IP address e.g. 192.168.1.x		
rcvip=0x0a 			# Last octet of the TCP receiver's IP address e.g. 192.168.1.x	
#####################

			

# Synchronization offsets are passed to python scripts : TO ADAPT !!
# Please check ./capture.pcap file and compare with the values below for a hint of how offsets are measured

#######################
sync_ul_back=0.000147 # Time of the reception of the first Block ack (relative to the transmission of the first TCP data segment)
sync_ul_ack=0.000277  # Time of the reception of first TCP ack
sync_dl_back=0.000305 # Time of the transmission of the first Block ack (that acknowledges the first TCP ack)
#######################


SENDER=./tcp_sender			
RECEIVER=./tcp_receiver		
TR=$1			
EXT=./extractors			
SEQ=./sequences	



# Filter Block Ack coming from TCP receiver 
tcpdump -ttttt -xx -r $TR "wlan[0:1] == 0x94 && wlan[16:1] == 0x05 && wlan[13:2]==${rcvmac}"  > $RECEIVER/back-tcprcv.str
tcpdump -ttttt -xx -r $TR "wlan[0:1] == 0x94 && wlan[16:1] == 0x05 && wlan[13:2]==${rcvmac}"  -w $RECEIVER/back-tcprcv.pcap

# Filter Block Ack coming from TCP sender
tcpdump -ttttt -xx -r $TR "wlan[0:1] == 0x94 && wlan[16:1] == 0x05 && wlan[13:2]==0x0a9c"  > $SENDER/back-tcpsnd.str
tcpdump -ttttt -xx -r $TR "wlan[0:1] == 0x94 && wlan[16:1] == 0x05 && wlan[13:2]==0x0a9c"  -w $SENDER/back-tcpsnd.pcap

# Filter packets (TCP segments and acks) coming from TCP receiver
tcpdump -ttttt -xx -r $TR "wlan[0:1]==0x88 && ip[15:1]==${rcvip} && ip[9:1]==0x06" > $RECEIVER/ip-tcprcv.str 
tcpdump -ttttt -xx -r $TR "wlan[0:1]==0x88 && ip[15:1]==${rcvip} && ip[9:1]==0x06" -w $RECEIVER/ip-tcprcv.pcap

# Filter packets (TCP segments and acks) coming from TCP sender
tcpdump -ttttt -xx -r $TR "wlan[0:1]==0x88 && ip[15:1]==${sndip} && ip[9:1]==0x06" > $SENDER/ip-tcpsnd.str 
tcpdump -ttttt -xx -r $TR "wlan[0:1]==0x88 && ip[15:1]==${sndip} && ip[9:1]==0x06" -w $SENDER/ip-tcpsnd.pcap


# Extract data frames' sequence space 
python3 $EXT/frame_seq.py $RECEIVER/ip-tcprcv.str $SEQ/frame_tcprcv.seq $sync_ul_ack
python3 $EXT/frame_seq.py $SENDER/ip-tcpsnd.str $SEQ/frame_tcpsnd.seq 0
 
# Extract Block Ack frames' sequence space 
python3 $EXT/back_seq.py $RECEIVER/back-tcprcv.str $SEQ/back_tcprcv.seq $sync_ul_back
python3 $EXT/back_seq.py $SENDER/back-tcpsnd.str $SEQ/back_tcpsnd.seq $sync_dl_back

# Extract TCP ack sequence space
python3 $EXT/ack_seq.py $RECEIVER/ip-tcprcv.str $SEQ/ack_tcprcv.seq $sync_ul_ack

# Extract TCP segement space sequence
python3 $EXT/segment_seq.py $SENDER/ip-tcpsnd.str $SEQ/seg_tcpsnd.seq 0

echo
echo "Data Extraction ==> Done !"


