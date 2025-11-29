# 🛡️ Vuln-Hunter: Automated Web Vulnerability Scanner

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Security](https://img.shields.io/badge/Security-SQLi%20%26%20XSS-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Stable-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

> **Next-generation, multi-threaded, and modular web vulnerability scanner designed for modern web applications.**

---

## 🎯 Business Value & Purpose

In the cybersecurity landscape, the most costly data breaches often stem from simple, overlooked entry points. **Vuln-Hunter** is engineered to automate the reconnaissance and scanning phases of Penetration Testing, bridging the gap between manual auditing and automated security.

This tool empowers Security Engineers and Developers to:
* **Reduce Time-to-Detect:** Automates hours of manual form testing into minutes using multi-threading.
* **Identify Critical Risks:** Detects high-impact **SQL Injection** (Database compromise) and **XSS** (Client-side attacks) vulnerabilities with high precision.
* **Actionable Reporting:** Generates professional HTML reports with OWASP-compliant remediation steps for non-technical stakeholders.

## 🚀 Key Features

* 🕷️ **Multi-Threaded Crawler:** Rapidly maps the target website, identifying hidden endpoints and assets.
* 🧠 **Smart Form Analysis:** Intelligently recognizes input types (`password`, `email`, `hidden`) and injects context-aware payloads.
* 💉 **Advanced Payload Injection:** Utilizes a curated list of polyglot payloads to bypass basic WAFs (Web Application Firewalls).
* 🛡️ **Proxy Support:** Seamlessly integrates with tools like **Burp Suite** or **OWASP ZAP** for traffic analysis.
* 📊 **Professional Reporting:** Produces detailed HTML reports categorized by severity (Critical/High) with direct remediation guidance.
* 🔄 **Resilient Architecture:** Implements auto-retry logic and error handling for unstable network conditions.

## 🛠️ Installation

Clone the repository and install the required dependencies:

```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/vuln-hunter.git](https://github.com/YOUR_USERNAME/vuln-hunter.git)

# Navigate to the project directory
cd vuln-hunter

# Install requirements
pip install -r requirements.txt
💻 Usage
Vuln-Hunter is controlled via a Command Line Interface (CLI) for easy integration into CI/CD pipelines.

Basic Scan:

Bash

python run.py -u [http://testphp.vulnweb.com](http://testphp.vulnweb.com)
High-Speed Scan (10 Threads):

Bash

python run.py -u [http://testphp.vulnweb.com](http://testphp.vulnweb.com) -t 10
Scan via Proxy (e.g., Burp Suite):

Bash

python run.py -u [http://target.com](http://target.com) -p [http://127.0.0.1:8080](http://127.0.0.1:8080)
📂 Project Architecture
The project follows a Modular Architecture to ensure maintainability and scalability.

vuln-hunter/
├── core/
│   ├── crawler.py    # Multi-threaded crawler & link discovery engine
│   ├── scanner.py    # Vulnerability detection & payload injection engine
│   ├── payloads.py   # Database of SQLi & XSS attack vectors
│   ├── report.py     # HTML reporting module
│   └── session.py    # HTTP session management with Retry logic
├── run.py            # Main entry point (CLI)
├── requirements.txt  # Project dependencies
└── README.md         # Documentation
📊 Sample Report
Upon completion, the tool generates a Pentest_Report.html file containing:

Vulnerability Type: (e.g., SQL Injection)

Affected URL: The specific endpoint vulnerable to attack.

Payload: The exact injection string that triggered the vulnerability.

Remediation: Technical advice for developers (e.g., "Implement Prepared Statements").

⚠️ Disclaimer
This software is developed for educational purposes and authorized security testing only. Usage of this tool for attacking targets without prior mutual consent is illegal. The developer assumes no liability and is not responsible for any misuse or damage caused by this program.

Developer: Gökhan Can