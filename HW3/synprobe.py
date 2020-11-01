import sys
from scapy.all import *

target = ""
ports = [21, 23, 25, 53, 80] # default ports

# synprobe.py target
if len(sys.argv) == 2:
    target = sys.argv[1]
    # print(ports)
    # print(target)

# synprobe.py -p port target
if len(sys.argv) == 4:
    ports = sys.argv[2]
    target = sys.argv[3]
    if "-" in ports: # start-end
        start, end = ports.split("-")
        start = int(start)
        end = int(end)
        ports = []
        for i in range(start, end+1):
            ports.append(i)
    elif "," in ports: # x,y,z
        ports = ports.split(",")
        for i in range(len(ports)):
            ports[i] = int(ports[i])
    else: # x
        ports = [int(ports)]
    # print(ports)
    # print(target)

print("PORT STATUS  FINGERPRINT")
for port in ports:
    packet = IP(dst=target)/TCP(dport=port, flags="S")
    response = sr1(packet, timeout=0.5, verbose=0)
    if response==None:
        print("response==None")
        continue
    if response.haslayer(TCP) and response.getlayer(TCP).flags=="SA":
        string = str(port)+"  open  " + "1234567890"
        print(string)
    sr(IP(dst=target)/TCP(dport=response.sport, flags="R"), timeout=0.5, verbose=0)







