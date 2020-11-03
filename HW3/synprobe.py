import sys
import socket
import ipaddress
from scapy.all import *

# helper function
def checkres(response):
    if response == None:
        return None
    elif response.haslayer(TCP) and response.getlayer(TCP).flags=="SA":
        return "open"
    elif response.haslayer(TCP) and response.getlayer(TCP).flags=="RA":
        return "closed"

# I watched this tutorial https://www.youtube.com/watch?v=4Y-MR-Hec5Y&ab_channel=CristiVlad on how to build a port scanner
# I learned the concepts, got inspiration, and then coded the majority of the function on my own.
# I also referred to the official documentation for scapy quite often:
# https://0xbharath.github.io/art-of-packet-crafting-with-scapy/network_recon/service_discovery/index.html
def scan(target):
    print("==============================")
    print("Scanning "+target)
    print("PORT STATUS  FINGERPRINT")
    for port in ports:
        # print("Port: "+str(port))
        packet = IP(dst=target)/TCP(dport=port, flags="S")
        response = sr1(packet, timeout=0.5, verbose=0)
        if checkres(response)==None:
            string = str(port) + "  filtered"
            print(string)
        elif checkres(response)=="open":
            synack_packet_bytes = bytes(response)
            response = ""
            timeout = False
            gotresponse = False
            for i in range(3):
                # The following code snippet use socket to connect to the port and send a dummy request
                # The source of the code snippet is https://stackoverflow.com/questions/34192093/python-socket-get
                s = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)
                s.connect((target, port))
                s.settimeout(2**i)
                request = "GET / HTTP/1.1\r\nHost: "+target+"\r\n\r\n"
                s.sendall(request.encode(encoding='utf-8')) # https://stackoverflow.com/questions/43237853/python-typeerror-a-bytes-like-object-is-required-not-str
                try:
                    response = s.recv(1024)
                    if len(response) != 0:
                        gotresponse = True
                        s.close()
                        break
                except socket.timeout:
                    timeout = True
                s.close()
            if gotresponse==True:
                fingerprint = synack_packet_bytes+bytes(response)
                if len(fingerprint) > 1024:
                    fingerprint = fingerprint[:1024] # keep only the first 1024 bytes
                string = str(port)+"  open  " + fingerprint.hex() # https://stackoverflow.com/questions/6624453/whats-the-correct-way-to-convert-bytes-to-a-hex-string-in-python-3/6624521
                print(string)
            else:
                string = str(port) + "  open  "+"Port: "+str(port)+", 3 requests transmitted, 0 bytes received"
                print(string)
        elif checkres(response)=="closed":
            string = str(port) + "  closed"
            print(string)
        # print("==============================")

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

    # Here for each port numbers format, I use different logic to extract the port numbers
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

if "/" in target: # if the target is a subnet
    ips = []
    for ip in ipaddress.IPv4Network(target): # https://stackoverflow.com/questions/13368659/how-can-i-loop-through-an-ip-address-range-in-python
        ips.append(str(ip))
    target = ips
else: # if the target is a single IP address
    target = [target]

if len(target) == 1:
    ip = target[0]
    scan(ip)
else:
    for ip in target: # if there are more than one IP address
        scan(ip)













