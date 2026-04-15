import socket
import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

def scan_port(target, port, timeout=0.5):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        result = sock.connect_ex((target, port))

        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"

            print(f"[OPEN] Port {port} ({service})")
            return {"port": port, "service": service}

        sock.close()

    except:
        pass

    return None


def scan_ports(target, ports, threads=100):
    print("\n" + "-" * 50)
    print(f"Scanning Target: {target}")
    print(f"Time: {datetime.now()}")
    print("-" * 50 + "\n")

    open_ports = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(lambda p: scan_port(target, p), ports)

        for r in results:
            if r:
                open_ports.append(r)

    # -------------------------
    # TEXT REPORT
    # -------------------------
    with open("results.txt", "w") as f:
        f.write(f"Scan Report\n")
        f.write(f"Target: {target}\n")
        f.write(f"Time: {datetime.now()}\n\n")

        for p in open_ports:
            f.write(f"OPEN PORT: {p['port']} ({p['service']})\n")

        f.write(f"\nTotal: {len(open_ports)} open ports\n")

    # -------------------------
    # JSON EXPORT (NEW)
    # -------------------------
    data = {
        "target": target,
        "time": str(datetime.now()),
        "open_ports_count": len(open_ports),
        "open_ports": open_ports
    }

    with open("results.json", "w") as f:
        json.dump(data, f, indent=4)

    print("\nScan Completed")
    print(f"Open Ports: {len(open_ports)}")
    print("Saved: results.txt + results.json")


def parse_ports(port_range):
    if "-" in port_range:
        start, end = map(int, port_range.split("-"))
        return range(start, end + 1)
    return [int(port_range)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", required=True)
    parser.add_argument("-p", "--ports", required=True)
    parser.add_argument("-T", "--threads", type=int, default=100)

    args = parser.parse_args()

    ports = parse_ports(args.ports)

    scan_ports(args.target, ports, args.threads)


if __name__ == "__main__":
    main()