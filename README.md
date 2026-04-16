# 🔐 Network Port Scanner (Python)

## 📌 Overview
This project is a Python-based multi-threaded TCP port scanner built for cybersecurity and networking practice.

It scans a target IP address or domain, identifies open ports, performs basic service detection, attempts banner grabbing, and exports results in both TXT and JSON formats.

---

## ⚙️ Features
- Multi-threaded TCP port scanning
- IP address and domain support
- Custom port ranges (e.g. 1-1000, 22,80,443)
- Basic service detection
- Banner grabbing (service response capture)
- Export results to TXT and JSON
- Timestamped scan reports
- Clean and readable CLI output

---

## 🚀 Example Usage
python scanner.py -t 127.0.0.1 -p 1-1000
python scanner.py -t scanme.nmap.org -p 22,80,443
python scanner.py -t 192.168.1.1 -p 1-1000 -T 200
python scanner.py -t 127.0.0.1 -p 20-100 --timeout 1

---

## 🧩 CLI Options
- -t, --target → Target IP address or domain
- -p, --ports → Port range or list
- -T, --threads → Number of worker threads
- --timeout → Socket timeout in seconds

---

## 📊 Sample Output
------------------------------------------------------------
Network Port Scanner
Target: 127.0.0.1
Resolved IP: 127.0.0.1
Started: 2026-04-16 09:15:30
Ports to scan: 3
Threads: 100
------------------------------------------------------------

[OPEN] Port 22 (ssh) | SSH-2.0-OpenSSH_8.9
[OPEN] Port 80 (http) | HTTP/1.1 200 OK
[OPEN] Port 443 (https) | No banner

Scan completed
Open ports found: 3
TXT report: scan_127.0.0.1_20260416_091530.txt
JSON report: scan_127.0.0.1_20260416_091530.json

---

## 📁 JSON Report Example
{
  "target": "127.0.0.1",
  "resolved_ip": "127.0.0.1",
  "started_at": "2026-04-16 09:15:30",
  "finished_at": "2026-04-16 09:15:31",
  "duration_seconds": 1.04,
  "ports_scanned": 3,
  "threads": 100,
  "timeout": 0.5,
  "open_ports_count": 2,
  "open_ports": [
    {
      "port": 22,
      "service": "ssh",
      "banner": "SSH-2.0-OpenSSH_8.9",
      "state": "open",
      "target": "127.0.0.1",
      "ip": "127.0.0.1"
    }
  ]
}

---

## ⚠️ Limitations
- TCP connect scan only
- Service detection is basic
- Banner grabbing depends on service response
- HTTPS banners may be limited

---

## 👤 Author
Ryadh Seddiki  
Cybersecurity Student | Network and Application Security Enthusiast  
GitHub: ryadhsed6

---

## ⚠️ Disclaimer
Educational use only. Do not scan systems you do not own or have permission to test.