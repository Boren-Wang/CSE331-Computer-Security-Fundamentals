import sys
from scapy.all import *

# read system arguments
interface = ""

if len(sys.argv) == 1: # arpwatch.py
    interface = "eth0"  # default network interface
elif len(sys.argv) == 3: # arpwatch.py [-i interface]
    interface = sys.argv[2]

# read the ip-mac mapping for the specified network interface
arp_cache = os.popen("arp -a") # https://www.tek-tips.com/viewthread.cfm?qid=1546657
records = {}
for record in arp_cache:
    if interface in record:
        ip = record.split(") at ")[0].split(" (")[1]
        mac=record.split(") at ")[1].split(" [")[0]
        records[ip] = mac

# helper function
def checkrecord(packet):
    if packet.haslayer(ARP) and packet.getlayer(ARP).op == 2: # The packet is an is-at ARP reply
        ip = packet.getlayer(ARP).psrc # sourcr ip address of the ARP reply
        mac = packet.getlayer(ARP).hwsrc # source mac address of the ARP reply
        if ip in records:
            real_mac = records[ip]
            if mac != real_mac: # if the proposed mac address of the ARP packet does not match with the record
                print("[alert] "+ip+" changed from "+real_mac+" to "+mac)
        else: # new ARP record
            records[ip] = mac
            # print("New ARP entry added to the cache: "+ip+" at "+mac+" on "+interface)

# sniff packets
sniff(store=False, prn=checkrecord)