import socket
from helpers import *
from _thread import start_new_thread

# Configuration
UDP_IP_ADDRESS = "172.18.2.0"  # IP address to listen on
UDP_PORT_NO = 53  # Port for DNS communication

# Create a UDP socket and bind it to the specified IP address and port
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverSock.bind((UDP_IP_ADDRESS, UDP_PORT_NO))

# Create a set to store blocked domain names
blocked_domains = set()
# Read the list of blocked domains from a file and populate the set
with open("blocked_domain.txt", "r") as f:
    for line in f:
        blocked_domains.add(line.strip())

def processReponse(data, addr):
    # Parse the incoming DNS query
    query = Query.fromBytes(data)
    print("Requested Domains:", query.domainName(), end="")

    if query.domainName() in blocked_domains:
        # If the requested domain is in the blocked list, block the request
        print("\t\tBlocked")
        # Send a blank response to the client
        serverSock.sendto(blankResponse(data, query), addr)
    else:
        print("\t\tAllowed")
        # Proxy the DNS query to an actual DNS server (127.0.0.53)
        DNS = "127.0.0.53"
        DNS_PORT = 53
        DNS_SERVER = (DNS, DNS_PORT)

        # Create a socket to communicate with the DNS server
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(DNS_SERVER)

        # Forward the DNS query to the DNS server
        sock.send(data)
        # Receive the response from the DNS server
        response = sock.recv(512)
        sock.close()

        # Send the DNS response back to the client
        serverSock.sendto(response, addr)

# Listener loop to continuously receive and process DNS queries
while True:
    data, addr = serverSock.recvfrom(512)
    # Start a new thread to process the DNS query
    start_new_thread(processReponse, (data, addr))
