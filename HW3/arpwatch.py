import sys
from scapy.all import *

# read system arguments
interface = ""
# arpwatch.py [-i interface]
if len(sys.argv) == 1:
    interface = "eth0"  # default network interface
elif len(sys.argv) == 3:
    interface = sys.argv[2]



# read the ip-mac mapping for the specified network interface
arp_cache = os.popen("arp -a") # https://www.tek-tips.com/viewthread.cfm?qid=1546657
records = {}
for record in arp_cache:
    if interface in record:
        ip = ""
        mac=""
        records[ip] = mac

# helper function


# sniff packets