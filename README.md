# 🔐 Network Port Scanner (Python)

## 📌 Overview
This is a Python-based multi-threaded port scanner that checks for open TCP ports on a target IP address or domain.

It is designed as a cybersecurity learning project to demonstrate basic network reconnaissance and socket programming skills.

---

## ⚙️ Features
- Scan IP addresses or domain names
- Custom port range support using CLI arguments
- Detect open TCP ports
- Multi-threaded scanning for faster performance
- Export results to `results.txt`
- Clean and structured terminal output

---

## 🧠 What I learned
- Networking fundamentals (IP addresses, ports, TCP connections)
- Socket programming in Python
- Multi-threading for performance improvement
- Command-line argument handling using argparse
- Error handling and input validation
- Building CLI-based cybersecurity tools

---

## 🚀 How to run

### Basic usage:
```bash
python scanner.py -t google.com -p 1-1000