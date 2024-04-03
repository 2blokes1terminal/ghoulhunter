from io import BytesIO
from tqdm import tqdm

import requests
import datetime
import zipfile
import base64
import json
import re

def scan(keywords, time, input_file):
    if input_file is None:
        now = datetime.datetime.now()
        month = str(now.month).zfill(2)
        day = str(now.day-time-1).zfill(2)
        datezip = base64.b64encode(f'{now.year}-{month}-{day}.zip'.encode()).decode()

        print('[nrdghoul - INFO] downloading nrds for yesterday')
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
            print("[nrdghoul - ERR] failed to download nrd list")
            return []

        zip = zipfile.ZipFile(content)
        print('[nrdghoul - OK] downloaded nrd list')

        for name in zip.namelist():
            if name == "domain-names.txt":
                domain_list = zip.read(name)
        
        try:
            domain_list = [x.decode() for x in domain_list.split()]
        except:
            domain_list = []
    else:
        if input_file.split('.')[-1] == 'ndjson': # domaintools file
            with open(input_file, 'r') as in_file:
                domain_list = [json.loads(x.strip())["message"]["domain"][0:-1] for x in in_file.readlines()]
        else:
            with open(input_file, 'r') as in_file:
                domain_list = [x.strip() for x in in_file.readlines()]

    results = []
    for keyword in keywords:
        regex = re.compile(keyword)

        results.extend(list(filter(lambda domain: check_domain(regex, domain), domain_list)))
    results = list(set(results))
    results.sort()
    
    return results

def check_domain(regex, domain):
    return re.search(regex, domain)

if __name__ == "__main__":
    pass
