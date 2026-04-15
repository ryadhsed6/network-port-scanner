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

```bash
python scanner.py -t google.com -p 1-1000
python scanner.py -t 127.0.0.1 -p 1-1000
python scanner.py -t 192.168.1.1 -p 20-500
```

---

## 📊 Example output

```
[OPEN] Port 22
[OPEN] Port 80
[OPEN] Port 443

Total OPEN ports: 3
```

---

## 🛡️ Future Improvements
- Add service detection (SSH, HTTP, FTP banners)
- Export results in JSON and CSV formats
- Improve performance using async scanning
- Add colored terminal output
- Add progress bar
- Add stealth scan modes

---

## 👤 Author
**Ryadh Seddiki**  
Cybersecurity Student | Network & Application Security Enthusiast  
GitHub: https://github.com/ryadhsed6

---

## ⚠️ Disclaimer
This tool is for educational purposes only.  
Do not use it on systems you do not own or have permission to test.