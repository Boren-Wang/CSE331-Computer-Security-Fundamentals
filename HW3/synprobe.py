import sys
from scapy.all import *
import socket

# helper function
def checkres(response):
    if response == None:
        return None
    elif response.haslayer(TCP) and response.getlayer(TCP).flags=="SA":
        return "open"
    elif response.haslayer(TCP) and response.getlayer(TCP).flags=="RA":
        return "closed"

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
    # print("Port: "+str(port))
    packet = IP(dst=target)/TCP(dport=port, flags="S")
    response = sr1(packet, timeout=0.5, verbose=0)
    if checkres(response)==None:
        gotresponse = False
        for i in range(3):
            res = sr1(packet, timeout=0.5, verbose=0)
            if checkres(res)=="open":
                string = str(port) + "  open  " + "1234567890"
                print(string)
                gotresponse=True
                break
            elif checkres(res)=="closed":
                string = str(port) + "  closed"
                print(string)
                gotresponse=True
                break
        if not gotresponse:
            string = str(port) + "  filtered  "+"Port: "+str(port)+", 3 requests transmitted, 0 bytes received"
            print(string)
    elif checkres(response)=="open":
        # ack_packet = IP(dst=target)/TCP(dport=port, flags="A")
        # ack_packet.seq = packet.seq + 1
        # ack_packet.ack = response.seq + 1
        # response = sr1(ack_packet, timeout=0.5, verbose=1)
        # response.show()
        # sr(IP(dst=target)/TCP(dport=response.sport, flags="R"), timeout=0.5, verbose=1) # drop the connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # https://stackoverflow.com/questions/34192093/python-socket-get
        s.connect((target, port))
        request = "GET / HTTP/1.1\r\nHost: "+target+"\r\n\r\n"
        s.sendall(request.encode(encoding='utf-8')) # https://stackoverflow.com/questions/43237853/python-typeerror-a-bytes-like-object-is-required-not-str
        response = s.recv(1024).hex() # https://stackoverflow.com/questions/6624453/whats-the-correct-way-to-convert-bytes-to-a-hex-string-in-python-3/6624521
        s.close
        string = str(port)+"  open  " + response
        print(string)
    elif checkres(response)=="closed":
        string = str(port) + "  closed"
        print(string)










