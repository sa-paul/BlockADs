# DNS-Based Ad Blocker Documentation

## Introduction
The DNS-Based Ad Blocker is a Python script that functions as a DNS proxy, intercepting incoming DNS queries and blocking requests to specific ad domains. It is designed to provide users on a network with ad-blocking functionality by rerouting DNS requests for known ad domains to a predefined IP address. The script works by parsing DNS queries, checking if the requested domain is in the list of blocked domains, and responding accordingly.

## Features
- Blocks DNS queries to ad domains specified in a blocklist.
- Acts as a DNS proxy for non-ad domain queries, forwarding them to an actual DNS server.
- Utilizes multi-threading to handle incoming DNS queries concurrently.

## Dependencies
- Python 3.x
- `socket` module
- `helpers` module (containing the `Query` and `blankResponse` functions)

## Setup and Usage

### 1. Configure IP Address and Port
- Edit the `UDP_IP_ADDRESS` and `UDP_PORT_NO` variables in the script to specify the IP address and port where the script will listen for incoming DNS queries.

### 2. Create Blocklist
- Create a text file named `blocked_domain.txt` and list the domain names to be blocked, each on a separate line.

### 3. Running the Script
1. Open a terminal window.
2. Navigate to the directory containing the script.
3. Run the script using the command:
   ```
   python script_name.py
   ```
   Replace `script_name.py` with the actual name of your script.

### 4. Testing
- Configure the DNS settings of devices on your network to use the IP address and port specified in the script as the DNS server. This can usually be done in the device's network settings.
- Observe the script's output as DNS queries are received and processed.

## How It Works

### DNS Query Processing (`processReponse` function)
1. The script listens for incoming DNS queries on the specified IP address and port.
2. Each query is processed in a new thread, providing concurrency.

### Blocked Domains
1. The script reads the `blocked_domain.txt` file to create a set of blocked domain names.
2. If a requested domain is found in the set of blocked domains, a blank DNS response is sent back to the client, effectively blocking the request.

### Non-Blocked Domains
1. If the requested domain is not in the set of blocked domains, the script functions as a DNS proxy.
2. It forwards the DNS query to an actual DNS server (127.0.0.53) using a new socket.
3. The response received from the DNS server is sent back to the client, allowing access to the requested non-ad domain.

## Note
- This script provides basic ad-blocking functionality and is intended for educational purposes. Production-level solutions may require additional features, security measures, and optimizations.
- Care should be taken to handle multi-threading and network operations safely to avoid potential issues.

## Conclusion
The DNS-Based Ad Blocker script demonstrates a simple approach to blocking ads on a network by intercepting DNS queries. It serves as a starting point for understanding DNS manipulation and proxying in Python.
