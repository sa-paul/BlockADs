import socket
from helpers import *
from _thread import start_new_thread

# Docs : https://datatracker.ietf.org/doc/html/rfc1035

UDP_IP_ADDRESS = "172.18.1.62"
UDP_PORT_NO = 12000


serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

blocked_domains = set()
with open("blocked_domain.txt", "r") as f:
    for line in f:
        blocked_domains.add(line.strip())

def processReponse(data, addr):
    query = Query.fromBytes(data)
    print(query.domainName())
    if blocked_domains.__contains__(query.domainName()):
        serverSock.sendto(blankResponse(data, query), addr)
    else:
        DNS="127.0.0.53"
        DNS_PORT=53
        DNS_SERVER=(DNS,DNS_PORT)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(DNS_SERVER)

        sock.send(data)
        response = sock.recv(512)
        sock.close()
        serverSock.sendto(response, addr)


# Listener
while True:
    data, addr = serverSock.recvfrom(512)
    start_new_thread(processReponse, (data, addr))