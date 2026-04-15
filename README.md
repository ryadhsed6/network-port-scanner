# 🔐 Network Port Scanner (Python)

## 📌 Overview
This is a Python-based multi-threaded port scanner that checks for open TCP ports on a target IP address or domain.

It is designed as a cybersecurity learning project to demonstrate network reconnaissance, socket programming, threading performance, and basic security analysis concepts.

---

## ⚙️ Features
- Scan IP addresses or domain names
- Custom port range support via CLI
- Multi-threaded scanning for high performance
- Detect open TCP ports
- Basic service detection (SSH, HTTP, HTTPS)
- Export results to **TXT and JSON formats**
- Clean CLI output for readability

---

## 📁 Output Files
After each scan, two files are generated:
- `results.txt` → Human-readable report
- `results.json` → Structured data for analysis or automation

---

## 🧠 What I learned
- TCP/IP networking fundamentals
- Socket programming in Python
- Multi-threading for performance optimization
- Command-line interface (CLI) development
- JSON data handling and structured logging
- Error handling and scanning reliability
- Building cybersecurity tools from scratch

---

## 🚀 How to run

Basic scan:
python scanner.py -t 127.0.0.1 -p 1-1000

Scan router / network device:
python scanner.py -t 192.168.1.1 -p 1-1000

Faster scan (more threads):
python scanner.py -t 127.0.0.1 -p 1-1000 -T 200

---

## 📊 Example output
[OPEN] Port 22 (ssh)
[OPEN] Port 80 (http)
[OPEN] Port 443 (https)

Scan Completed
Open Ports: 3
Saved: results.txt + results.json

---

## 📄 JSON Output Example
{
  "target": "127.0.0.1",
  "time": "2026-04-15 12:00:00",
  "open_ports_count": 3,
  "open_ports": [
    {
      "port": 22,
      "service": "ssh"
    },
    {
      "port": 80,
      "service": "http"
    }
  ]
}

---

## 🛡️ Future Improvements
- Banner grabbing (service fingerprinting)
- Async scanning (even faster performance)
- Progress bar for scan status
- Colored terminal output
- Stealth scan modes
- Web dashboard (GUI interface)

---

## 👤 Author
**Ryadh Seddiki**  
Cybersecurity Student | Network & Application Security Enthusiast  
GitHub: https://github.com/ryadhsed6

---

## ⚠️ Disclaimer
This tool is for educational purposes only.  
Do not use it on systems you do not own or have explicit permission to test.