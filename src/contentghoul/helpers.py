import socket
import whoisit

print("[contentghoul - INFO] bootstrapping whois")
whoisit.bootstrap()

def get_ip_org(ip):
    return whoisit.ip(ip)

def get_domain_org(domain):
    pass

def resolve_domain(domain):
    try:
        ip = socket.gethostbyname_ex(domain)
        ip4 = ip[2]
        ip6 = ip[1]
        return ((ip4, ip6), False)
    except socket.gaierror:
        print(f"[contentghoul - ERR] {domain} does not resolve. ignoring...")
        return (([], []), True)
