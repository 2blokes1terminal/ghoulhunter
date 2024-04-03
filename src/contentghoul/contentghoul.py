# Comments from burgo2b1t:
# dodgey as fuck beautiful soup scraper that looks for html title
# to do - populate array from list of enumerated domains, scan html title for 
# mygov and report bool value

from contentghoul.helpers import *

import requests
from bs4 import BeautifulSoup


def scan_ip(domain):
    pass


def scan_domain(domain):
    print(f'[contentghoul - INFO] scanning {domain}')
    ip = resolve_domain(domain)

    if ip[1]:  # if error
        return {
            "ip": "",
            "ipv4_org": "",
            "ipv6_org": "",
            "http_scan_result": [],
            "can_resolve": False
        }

    ip = ip[0]
    ipv4_org = get_ip_org(ip[0][0])["name"] if ip[0] != [] else ""
    ipv6_org = get_ip_org(ip[1][0])["name"] if ip[1] != [] else ""

    try:
        https_content_result = scan_url(f"https://{domain}/")
    except:
        return {
            "ip": "",
            "ipv4_org": "",
            "ipv6_org": "",
            "http_scan_result": [],
            "can_resolve": False
        }

    return {
        "ip": ip,
        "ipv4_org": ipv4_org,
        "ipv6_org": ipv6_org,
        "http_scan_result": https_content_result,
        "can_resolve": True
    }


def scan_url(url):
    reqs = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/118.0"
        },
        verify=False,
        timeout=10
    )
    server = reqs.headers.get('server')

    # soupkitchen time
    soup = BeautifulSoup(reqs.text, 'html.parser')

    return {
        "titles": [
            title_element.get_text()
            for title_element
            in soup.find_all('title')
        ],
        "links": [
            link['href']
            for link
            in soup.find_all('a', href=True)
        ]
    }
