from io import BytesIO
import requests
import datetime
import zipfile
import base64
from tqdm import tqdm
import re

def scan(keywords):
    now = datetime.datetime.now()
    month = str(now.month).zfill(2)
    datezip = base64.b64encode(f'{now.year}-{month}-{now.day - 2}.zip'.encode()).decode()

    print('[.] downloading nrds for yesterday')
    req = requests.get(f'https://www.whoisds.com//whois-database/newly-registered-domains/{datezip}/nrd', stream=True)
    content_length = int(req.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=content_length, unit='iB', unit_scale=True, colour="green")

    content = BytesIO()
    for data in req.iter_content(block_size):
        progress_bar.update(len(data))
        content.write(data)
    progress_bar.close()

    if content_length != 0 and progress_bar.n != content_length:
        print("[!] failed to download nrd list")
        return []

    zip = zipfile.ZipFile(content)
    print('[*] downloaded nrd list')

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
