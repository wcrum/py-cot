import CoT
from scapy.all import *

packets = rdpcap("sample.pcap")
packets.summary()

for packet in packets:
    xml = packet.load.decode()
    try:
        event = CoT.Event(**CoT.xml.parse(xml))
        # do something with the event
    except:
        pass
