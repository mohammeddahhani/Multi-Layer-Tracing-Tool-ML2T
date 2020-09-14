# Introduction
A ML2T is a multi-layer tracing tool to analyse data transmission of the MAC and TCP layers on the same graph.

For now, only uniderectional TCP traffic is supported.

# Requirement
Our tool requires a vailde capture file which can produced using `tcpdump`. In case of a wireless network, monitor mode should be activated to capture the transient trafic.

The capture file should start with a TCP data segment, excluding TCP handshake segments (i.e. syn, syn-ack, ack)
This can be done by using wireshark build-in filtering: 
- If the starting TCP segment is captured at t = 49.1 seconds, `frame.time_relative >= 49.1` extracts all the trafic starting t= 49.1 s.
- `file -> Export specified`

# Usage
`./extract capture.pcap` To extract necessary data
For plotting:
- `python --to-segs` to plot mac frames and their associated block ack that encapsulate TCP segments
- or `python --to-acks` to plot mac frames and their associated block ack that encapsulate TCP acks

# Description
ML2T take as an input a pre-processed tcpdump capture (.pcap) to produces a set of data which can be used -- e.g. using python -- to create a Time/Sequence plot.

Files and folders relevent to how ML2T works are described bellow:

- __./tcp_sender__: Contains two capture files, one for block acks frames and the other one for packets sent by the TCP sender. The string version of each pcap files is also given

- __./tcp_receiver__: Contains two capture files, one for block acks frames and the other one for packets sent by the TCP receiver. The string version of each pcap files is also given

- __./sequences__: Contains MAC sequence numbers of all data frames sent by both the sender and receiver (frame_tcpxxx.seq), MAC sequence numbers and the content of the bitmap of block acks sent by both TCP sender and receiver (back_tcpxxx.seq) and finally the TCP sequence numbers of TCP sender segments (seg_tcpsnd.seq) and TCP receiver acks (ack_tcprcv.seq) 

- __./extractors__: a set of scripts that use the string version of the captures in ./tcp_sender and ./tcp_receiver to extract sequences at the MAC and TCP layer and store them in the ./sequence folder





