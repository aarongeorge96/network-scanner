\# Network Scanner



A Python tool to discover devices and open ports on your local network.



\## What It Does



1\. Finds your local IP address

2\. Scans all 254 IPs in your network range

3\. Identifies active devices

4\. Scans common ports on each device

5\. Resolves hostnames where possible



\## What You Can Learn



\- Which devices are on your network

\- What services each device is running

\- Potential security issues (open ports that shouldn't be)



\## Common Ports Scanned



| Port | Service | What It Means |

|------|---------|---------------|

| 21 | FTP | File transfer |

| 22 | SSH | Secure shell (remote access) |

| 23 | Telnet | Insecure remote access |

| 80 | HTTP | Web server |

| 135 | RPC | Windows Remote Procedure Call |

| 139 | NetBIOS | Windows networking |

| 443 | HTTPS | Secure web server |

| 445 | SMB | Windows file sharing |

| 3389 | RDP | Remote desktop |



\## Setup

```bash

git clone https://github.com/yourusername/network-scanner.git

cd network-scanner

python -m venv venv

venv\\Scripts\\activate  # Windows

pip install -r requirements.txt

```



\## Usage

```bash

python -m network\_scanner.scanner

```



\## Sample Output

```

Your IP: 192.168.1.67



Scanning network 192.168.1.0/24...

&nbsp; \[+] Found: 192.168.1.1

&nbsp; \[+] Found: 192.168.1.67

&nbsp; \[+] Found: 192.168.1.254



Host Details:

192.168.1.67 (LAPTOP-ABC123)

&nbsp; \[+] Port 135 (RPC) - OPEN

&nbsp; \[+] Port 445 (SMB) - OPEN



192.168.1.254

&nbsp; \[+] Port 53 (DNS) - OPEN

&nbsp; \[+] Port 80 (HTTP) - OPEN

```



\## Security Notes



\- Only scan networks you own or have permission to scan

\- Scanning without permission may be illegal

\- Use this tool for learning and securing your own network



\## Technologies



\- Python

\- Socket programming

\- Threading for parallel scanning

