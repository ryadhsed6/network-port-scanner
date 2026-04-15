import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

target = input("Enter target IP or domain: ")

print("-" * 50)
print(f"Scanning target: {target}")
print(f"\nTime started: {datetime.now()}")
print("-" * 50)

try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Error: Unable to resolve host.")
    exit()

print(f"IP Address: {target_ip}")
print("-" * 50)

# Function to scan a single port
from concurrent.futures import ThreadPoolExecutor, as_completed

open_ports = []

def scan_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.3)

    result = sock.connect_ex((target_ip, port))

    sock.close()

    if result == 0:
        return port
    return None


with ThreadPoolExecutor(max_workers=200) as executor:
    results = executor.map(scan_port, range(1, 1001))

    for port in results:
        if port is not None:
            open_ports.append(port)

print("\nRESULTS:")
print("-" * 30)

for port in open_ports:
    print(f"[OPEN] Port {port}")

print("-" * 30)
print(f"Total OPEN ports: {len(open_ports)}")

# Run multiple threads
with ThreadPoolExecutor(max_workers=100) as executor:
    for port in range(1, 1001):
        executor.submit(scan_port, port)

print("-" * 50)
print("Scan completed.")
print("-" * 50)