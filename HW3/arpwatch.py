import sys
from scapy.all import *

# read system arguments
interface = ""
# arpwatch.py [-i interface]
if len(sys.argv) == 1:
    interface = ""  # default network interface
elif len(sys.argv) == 3:
    interface = sys.argv[2]



# read the ip-mac mapping for the specified network interface
arp_cache = os.popen("arp -a") # https://www.tek-tips.com/viewthread.cfm?qid=1546657
for record in arp_cache:
    print(record)

# helper function


# sniff packets