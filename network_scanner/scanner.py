"""
Network Scanner - Discover devices and open ports on your network.
"""

import socket
import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor


def get_local_ip():
    """Get your computer's local IP address."""
    try:
        # Connect to external server to find local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"


def ping(ip):
    """
    Ping an IP address to check if it's alive.
    Returns True if host responds, False otherwise.
    """
    # Different ping command for Windows vs Linux/Mac
    param = "-n" if platform.system().lower() == "windows" else "-c"
    
    command = ["ping", param, "1", "-w", "1000", ip]
    
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception:
        return False


def scan_network(base_ip):
    """
    Scan all IPs in a /24 network (e.g., 192.168.1.1 to 192.168.1.254).
    Returns list of active IPs.
    """
    # Extract first three octets (e.g., "192.168.1" from "192.168.1.100")
    network = ".".join(base_ip.split(".")[:-1])
    
    print(f"Scanning network {network}.0/24...")
    print("This may take a minute...\n")
    
    active_hosts = []
    
    # Scan IPs 1-254 using multiple threads for speed
    ips_to_scan = [f"{network}.{i}" for i in range(1, 255)]
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(ping, ips_to_scan)
        
        for ip, is_active in zip(ips_to_scan, results):
            if is_active:
                print(f"  [+] Found: {ip}")
                active_hosts.append(ip)
    
    return active_hosts


def scan_port(ip, port):
    """
    Check if a specific port is open on an IP.
    Returns True if open, False if closed.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception:
        return False


def scan_common_ports(ip):
    """
    Scan common ports on a host.
    Returns list of open ports.
    """
    # Common ports and their services
    common_ports = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        135: "RPC",
        139: "NetBIOS",
        143: "IMAP",
        443: "HTTPS",
        445: "SMB",
        993: "IMAPS",
        995: "POP3S",
        3306: "MySQL",
        3389: "RDP",
        5432: "PostgreSQL",
        8080: "HTTP-Proxy"
    }
    
    print(f"\nScanning ports on {ip}...")
    
    open_ports = []
    
    for port, service in common_ports.items():
        if scan_port(ip, port):
            print(f"  [+] Port {port} ({service}) - OPEN")
            open_ports.append({"port": port, "service": service})
    
    if not open_ports:
        print("  No common ports open")
    
    return open_ports


def get_hostname(ip):
    """Try to get the hostname for an IP address."""
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except Exception:
        return None


if __name__ == "__main__":
    print("=" * 50)
    print("Network Scanner")
    print("=" * 50)
    
    # Get local IP
    local_ip = get_local_ip()
    print(f"\nYour IP: {local_ip}")
    
    # Scan network for active hosts
    active_hosts = scan_network(local_ip)
    
    print(f"\nFound {len(active_hosts)} active hosts")
    
    # Get hostnames and scan ports for each active host
    print("\n" + "=" * 50)
    print("Host Details")
    print("=" * 50)
    
    for ip in active_hosts:
        hostname = get_hostname(ip)
        if hostname:
            print(f"\n{ip} ({hostname})")
        else:
            print(f"\n{ip}")
        
        scan_common_ports(ip)