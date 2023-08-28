#ContentGhoul
#dodgey as fuck beautiful soup scraper that looks for html title 
#to do - populate array from list of enumerated domains, scan html title for mygov and report bool value

from contentghoul.helpers import *

import requests
from bs4 import BeautifulSoup

def scan_ip(domain):
    pass

def scan_domain(domain):
    print(f'[.] scanning {domain}')
    ip = resolve_domain(domain)
    ipv4_org = get_ip_org(ip[0][0])["name"] if ip[0] != [] else ""
    ipv6_org = get_ip_org(ip[1][0])["name"] if ip[1] != [] else ""

    print(ipv4_org)

    return (ip, ipv4_org, ipv6_org)

def scan_url(url):
    reqs = requests.get(url)   

    #soupkitchen time
    soup = BeautifulSoup(reqs.text, 'html.parser')

    return [title_element.get_text() for title_element in soup.find_all('title')]
