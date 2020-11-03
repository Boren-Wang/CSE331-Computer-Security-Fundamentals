import sys
from scapy.all import *

# read system arguments
interface = ""

if len(sys.argv) == 1: # arpwatch.py
    interface = "eth0"  # default network interface
elif len(sys.argv) == 3: # arpwatch.py [-i interface]
    interface = sys.argv[2]

# read the ip-mac mapping for the specified network interface
# !!!!!!!!!!I referenced this article https://www.tek-tips.com/viewthread.cfm?qid=1546657
# on how to use python’s os.popen() to execute “arp -a” to get the arp cache.!!!!!!!!!!
arp_cache = os.popen("arp -a") # from https://www.tek-tips.com/viewthread.cfm?qid=1546657
records = {}
for record in arp_cache: # from https://www.tek-tips.com/viewthread.cfm?qid=1546657
    if interface in record:
        ip = record.split(") at ")[0].split(" (")[1]
        mac=record.split(") at ")[1].split(" [")[0]
        records[ip] = mac

# helper function
# This function will check if a packet is an ARP reply and if an ARP reply's MAC matches with the ground truth records.
# !!!!!!!!!!This function is inspired by the process function in this article:
# https://www.thepythoncode.com/article/detecting-arp-spoof-attacks-using-scapy
# After I read the article on how to write a callback for sniff to process each packet, I wrote the checkrecord on my own!!!!!!!!!!
# I also referred to the official documentation for scapy quite often:
# https://0xbharath.github.io/art-of-packet-crafting-with-scapy/network_recon/service_discovery/index.html
def checkrecord(packet):
    if packet.haslayer(ARP) and packet.getlayer(ARP).op == 2: # The packet is an is-at ARP reply
        ip = packet.getlayer(ARP).psrc # sourcr ip address of the ARP reply
        mac = packet.getlayer(ARP).hwsrc # source mac address of the ARP reply
        if ip in records:
            real_mac = records[ip] # look uo the ground truth records
            if mac != real_mac: # if the proposed mac address of the ARP packet does not match with the record
                print("[alert] "+ip+" changed from "+real_mac+" to "+mac)
        else: # new ARP record
            records[ip] = mac
            # print("New ARP entry added to the cache: "+ip+" at "+mac+" on "+interface)

# sniff packets
# !!!!!!!!!!I learned from this article https://www.thepythoncode.com/article/detecting-arp-spoof-attacks-using-scapy
# about how to use scapy’s sniff() function to monitor and process each packet!!!!!!!!!!
sniff(store=False, prn=checkrecord)