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

def scan(target):
    print("==============================")
    print("Scanning "+target)
    print("PORT STATUS  FINGERPRINT")
    for port in ports:
        # print("Port: "+str(port))
        packet = IP(dst=target)/TCP(dport=port, flags="S")
        response = sr1(packet, timeout=0.5, verbose=0)
        if checkres(response)==None:
            gotresponse = False
            for i in range(2):
                timeout = 2**i
                res = sr1(packet, timeout=timeout, verbose=0)
                if checkres(res)=="open":
                    s = socket.socket(socket.AF_INET,
                                      socket.SOCK_STREAM)  # https://stackoverflow.com/questions/34192093/python-socket-get
                    s.connect((target, port))
                    request = "GET / HTTP/1.1\r\nHost: " + target + "\r\n\r\n"
                    s.sendall(request.encode(
                        encoding='utf-8'))  # https://stackoverflow.com/questions/43237853/python-typeerror-a-bytes-like-object-is-required-not-str
                    response = s.recv(
                        1024).hex()  # https://stackoverflow.com/questions/6624453/whats-the-correct-way-to-convert-bytes-to-a-hex-string-in-python-3/6624521
                    s.close()
                    string = str(port) + "  open  " + response
                    print(string)
                    gotresponse=True
                    break
                elif checkres(res)=="closed":
                    string = str(port) + "  closed"
                    print(string)
                    gotresponse=True
                    break
            if not gotresponse:
                string = str(port) + "  filtered"
                print(string)
        elif checkres(response)=="open":
            synack_packet_bytes = bytes(response)
            response = ""
            timeout = False
            gotresponse = False
            for i in range(3):
                s = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)  # https://stackoverflow.com/questions/34192093/python-socket-get
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
                    fingerprint = fingerprint[:1024]
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

if "/" in target: # if the target is a subnet https://stackoverflow.com/questions/13368659/how-can-i-loop-through-an-ip-address-range-in-python
    ips = []
    for ip in ipaddress.IPv4Network(target):
        ips.append(str(ip))
    target = ips
else:
    target = [target]

if len(target) == 1:
    ip = target[0]
    scan(ip)
else:
    for ip in target:
        scan(ip)













