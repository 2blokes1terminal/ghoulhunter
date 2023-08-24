#ContentGhoul
#dodgey as fuck beautiful soup scraper that looks for html title 
#to do - populate array from list of enumerated domains, scan html title for mygov and report bool value

import requests
from bs4 import BeautifulSoup

def scan_url(url):
    reqs = requests.get(url)   

    #soupkitchen time
    soup = BeautifulSoup(reqs.text, 'html.parser')

    print('html title of', url)

    for title in soup.find_all('title'):
        print(title.get_text())
