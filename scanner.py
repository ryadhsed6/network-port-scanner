import argparse
import socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description="Simple Python Port Scanner")

parser.add_argument("-t", "--target", help="Target IP or domain", required=True)
parser.add_argument("-p", "--ports", help="Port range (default 1-1000)", default="1-1000")

args = parser.parse_args()

target = args.target
port_range = args.ports

start_port, end_port = map(int, port_range.split("-"))

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
def scan_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.3)

    result = sock.connect_ex((target_ip, port))
    sock.close()

    if result == 0:
        return port
    return None

open_ports = []

with ThreadPoolExecutor(max_workers=200) as executor:
    results = executor.map(scan_port, range(start_port, end_port + 1))

    for port in results:
        if port is not None:
            open_ports.append(port)

print("\nRESULTS:")
print("-" * 30)

# Saves the results in file named results.txt
with open("results.txt", "w") as file:
    file.write(f"Scan results for {target} ({target_ip})\n")
    file.write("-" * 40 + "\n")

    for port in open_ports:
        file.write(f"OPEN PORT: {port}\n")

    file.write("-" * 40 + "\n")
    file.write(f"Total OPEN ports: {len(open_ports)}\n")

for port in open_ports:
    print(f"[OPEN] Port {port}")

print("-" * 30)
print(f"Total OPEN ports: {len(open_ports)}")

print("-" * 50)
print("Scan completed.")
print("-" * 50)