from io import BytesIO
import requests
import datetime
import zipfile
import base64
import re

def scan(keywords):
    now = datetime.datetime.now()
    month = str(now.month).zfill(2)
    datezip = base64.b64encode(f'{now.year}-{month}-{now.day - 2}.zip'.encode()).decode()

    req = requests.get(f'https://www.whoisds.com//whois-database/newly-registered-domains/{datezip}/nrd')

    content = BytesIO(req.content)
    zip = zipfile.ZipFile(content)

    for name in zip.namelist():
        if name == "domain-names.txt":
            domain_list = zip.read(name)
    
    try:
        domain_list = domain_list.split()
    except:
        domain_list = []

    results = []
    for keyword in keywords:
        regex = re.compile(keyword)

        results.extend([x.decode() for x in list(filter(lambda domain: check_domain(regex, domain.decode()), domain_list))])
    results = list(set(results))
    results.sort()
    
    return results

def check_domain(regex, domain):
    return re.search(regex, domain)

if __name__ == "__main__":
    pass
