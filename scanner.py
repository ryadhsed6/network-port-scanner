import argparse
import json
import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from time import perf_counter


def resolve_target(target):
    try:
        return socket.gethostbyname(target)
    except socket.gaierror as error:
        raise ValueError(f"Could not resolve target '{target}': {error}") from error


def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except OSError:
        return "unknown"


def build_probe(service, target):
    probes = {
        "http": f"HEAD / HTTP/1.0\r\nHost: {target}\r\n\r\n",
        "https": f"HEAD / HTTP/1.0\r\nHost: {target}\r\n\r\n",
        "smtp": "EHLO scanner.local\r\n",
        "pop3": "QUIT\r\n",
        "ftp": "QUIT\r\n",
    }
    return probes.get(service, "")


def grab_banner(target, port, timeout, service):
    try:
        with socket.create_connection((target, port), timeout=timeout) as sock:
            sock.settimeout(timeout)
            probe = build_probe(service, target)

            if probe:
                sock.sendall(probe.encode())

            banner = sock.recv(1024).decode(errors="ignore").strip()
            return banner or "No banner"
    except (socket.timeout, ConnectionError, OSError):
        return "No banner"


def scan_port(target_ip, target_label, port, timeout=0.5):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((target_ip, port))

        if result != 0:
            return None

        service = get_service_name(port)
        banner = grab_banner(target_ip, port, timeout, service)

        return {
            "port": port,
            "service": service,
            "banner": banner,
            "state": "open",
            "target": target_label,
            "ip": target_ip,
        }
    except OSError:
        return None


def validate_port(port):
    if not 1 <= port <= 65535:
        raise ValueError(f"Port '{port}' is out of range. Use values between 1 and 65535.")


def parse_ports(port_input):
    ports = set()

    for part in port_input.split(","):
        segment = part.strip()
        if not segment:
            continue

        if "-" in segment:
            try:
                start, end = map(int, segment.split("-", maxsplit=1))
            except ValueError as error:
                raise ValueError(f"Invalid port range: '{segment}'") from error

            if start > end:
                raise ValueError(f"Invalid port range: '{segment}'")

            for port in range(start, end + 1):
                validate_port(port)
                ports.add(port)
        else:
            try:
                port = int(segment)
            except ValueError as error:
                raise ValueError(f"Invalid port value: '{segment}'") from error

            validate_port(port)
            ports.add(port)

    if not ports:
        raise ValueError("No valid ports were provided.")

    return sorted(ports)


def sanitize_filename(value):
    return "".join(char if char.isalnum() or char in ("-", "_", ".") else "_" for char in value)


def build_output_paths(target):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_target = sanitize_filename(target)
    base_name = f"scan_{safe_target}_{timestamp}"
    return Path(f"{base_name}.txt"), Path(f"{base_name}.json")


def save_txt_report(report, txt_path):
    with txt_path.open("w", encoding="utf-8") as file:
        file.write("NETWORK PORT SCAN REPORT\n")
        file.write("=" * 60 + "\n")
        file.write(f"Target: {report['target']}\n")
        file.write(f"Resolved IP: {report['resolved_ip']}\n")
        file.write(f"Scan Started: {report['started_at']}\n")
        file.write(f"Scan Finished: {report['finished_at']}\n")
        file.write(f"Duration: {report['duration_seconds']:.2f} seconds\n")
        file.write(f"Ports Scanned: {report['ports_scanned']}\n")
        file.write(f"Threads: {report['threads']}\n")
        file.write(f"Timeout: {report['timeout']} seconds\n")
        file.write(f"Open Ports Found: {report['open_ports_count']}\n\n")

        if report["open_ports"]:
            for port_data in report["open_ports"]:
                file.write(
                    f"[OPEN] Port {port_data['port']} ({port_data['service']}) | {port_data['banner']}\n"
                )
        else:
            file.write("No open ports were detected in the selected range.\n")


def save_json_report(report, json_path):
    with json_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)


def scan_ports(target, ports, threads=100, timeout=0.5):
    target_ip = resolve_target(target)
    started_at = datetime.now()
    start_time = perf_counter()

    print("\n" + "-" * 60)
    print("Network Port Scanner")
    print(f"Target: {target}")
    print(f"Resolved IP: {target_ip}")
    print(f"Started: {started_at.isoformat(sep=' ', timespec='seconds')}")
    print(f"Ports to scan: {len(ports)}")
    print(f"Threads: {threads}")
    print("-" * 60 + "\n")

    open_ports = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = executor.map(lambda port: scan_port(target_ip, target, port, timeout), ports)

        for result in results:
            if result:
                open_ports.append(result)

    open_ports.sort(key=lambda item: item["port"])

    finished_at = datetime.now()
    duration = perf_counter() - start_time

    report = {
        "target": target,
        "resolved_ip": target_ip,
        "started_at": started_at.isoformat(sep=" ", timespec="seconds"),
        "finished_at": finished_at.isoformat(sep=" ", timespec="seconds"),
        "duration_seconds": round(duration, 2),
        "ports_scanned": len(ports),
        "threads": threads,
        "timeout": timeout,
        "open_ports_count": len(open_ports),
        "open_ports": open_ports,
    }

    txt_path, json_path = build_output_paths(target)
    save_txt_report(report, txt_path)
    save_json_report(report, json_path)

    for port_data in open_ports:
        print(f"[OPEN] Port {port_data['port']} ({port_data['service']}) | {port_data['banner']}")

    print("\nScan completed")
    print(f"Open ports found: {len(open_ports)}")
    print(f"TXT report: {txt_path.name}")
    print(f"JSON report: {json_path.name}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Multi-threaded TCP port scanner with banner grabbing and report export."
    )
    parser.add_argument("-t", "--target", required=True, help="Target IP address or domain name")
    parser.add_argument(
        "-p",
        "--ports",
        required=True,
        help="Port selection, for example: 22,80,443 or 1-1000",
    )
    parser.add_argument(
        "-T",
        "--threads",
        type=int,
        default=100,
        help="Number of worker threads to use (default: 100)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=0.5,
        help="Socket timeout in seconds (default: 0.5)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.threads < 1:
        raise SystemExit("Thread count must be at least 1.")

    try:
        ports = parse_ports(args.ports)
        scan_ports(args.target, ports, args.threads, args.timeout)
    except ValueError as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()