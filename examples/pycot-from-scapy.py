import CoT
from scapy.all import *

# local address, remove line if external
INTERFACE = "\\Device\\NPF_Loopback"


def PacketToCoT(packet):
    xml = packet.load.decode()
    try:
        event = CoT.Event(**CoT.xml.parse(xml))
        # do something with the event
    except:
        pass


SNIFFER = sniff(
    filter="port 4242",  # BFP Filter TAK Port 4242
    prn=PacketToCoT,
    store=0,  # dont store packets in SNIFFER
    iface=INTERFACE,  # local address, remove line if external
)
