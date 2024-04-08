#! /usr/bin/env python3

from screenshotghoul import screenshotghoul
from contentghoul import contentghoul
from fingerghoul import fingerghoul
from gapihunter import gapihunter
from nrdghoul import nrdghoul

from pyppeteer import launch
import pyppeteer
import argparse
import requests
import asyncio
import json
import sys
import os

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def output_results(data, teams_webhook):
    if teams_webhook is not None:
        newline = '\n'
        teams_json = {
            "type": "TextBlock",
            "text": '\n'.join([
                f"""

# **Result {i + 1}: {result['domain']}**


IPs: {' '.join([' '.join(x) for x in result['contentghoul_result']['ip']])}

IP Organisation: {result['contentghoul_result']['ipv4_org']} {result['contentghoul_result']['ipv6_org']}


Google API results:

```json
{json.dumps(result['gapihunter_result'], indent=2)}
```

| Fingerprints | Matches | Total Possible Matches | Positive |
| ------------ | ------- | ---------------------- | -------- |
{newline.join([
    f"| {x['name']} | {x['matches']} | {x['total']} | {x['positive']} |"
    for x in result['fingerghoul_result']
])}
"""
                for i, result in enumerate(data)
            ])
        }

        req = requests.post(json=teams_json, url=teams_webhook)
        print(teams_json)
        print(req)
    else:
        print(json.dumps(data, indent=2))


def main():
    parser = argparse.ArgumentParser(prog='ghoulhunter',
                                     description='hunt for phishing sites')
    parser.add_argument('--brand-keywords', '-k', nargs='+',
                        help='regex expression keywords')
    parser.add_argument('--domain', '-d',
                        help="Point ghoulhunter at a specific domain")
    parser.add_argument('--output-dir', '-o', help="Output directory",
                        default="output/")
    parser.add_argument('--time', '-t', help="Days back", default=1, type=int)
    parser.add_argument('--chrome-path', '-c',
                        help="Path to chrome executable",
                        default="/sbin/google-chrome-stable")
    parser.add_argument('--screenshot', '-s', help="Only screenshot domains",
                        action=argparse.BooleanOptionalAction)
    parser.add_argument('--list-domains', '-l', help="Only list domains found with nrdhunter",
                        action=argparse.BooleanOptionalAction)
    parser.add_argument('--input-file', '-i', help="Input domains from a file", type=str)
    parser.add_argument('--teams-webhook', '-w', help="Output results to a microsoft teams 'Incoming Webhook' adapter", type=str)
    args = parser.parse_args()

    if os.environ.get('GAPI_KEY') == "":
        print("[ghoulhunter - ERR] please set the GAPI_KEY environment variable")
        sys.exit(1)

    print(f"[ghoulhunter - INFO] starting ghoulhunter with args: {args}")
    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)

    async def get_browser():
        browser = await launch({
            "args":  ['--disable-gpu', '--disable-dev-shm-usage'],
            "executablePath": args.chrome_path
        })
        page = await browser.newPage()
        page.setDefaultNavigationTimeout(5000)
        return page
    page = asyncio.get_event_loop().run_until_complete(get_browser())

    final_results = []
    if args.list_domains:
        results = nrdghoul.scan(args.brand_keywords, args.time, args.input_file)

        print("\n".join(results))
    elif args.screenshot and args.domain is None:
        results = nrdghoul.scan(args.brand_keywords, args.time, args.input_file)
        for url in results:
            try:
                print(f'[screenshotghoul - INFO] screenshotting {url}')
                screenshotghoul.run_take_screenshot(url, page, args.output_dir)
            except pyppeteer.errors.PageError as e:
                print(f'[screenshotghoul - ERR] failed to screenshot domain \
                     {url}: {e}')
    elif args.domain is None:
        results = nrdghoul.scan(args.brand_keywords, args.time, args.input_file)
        for url in results:
            content_result = contentghoul.scan_domain(url)
            if content_result["can_resolve"] is False:
                continue

            finger_result = fingerghoul.scan_domain(url)
            gapi_result = gapihunter.check_url(url)

            try:
                screenshotghoul.run_take_screenshot(url, page, args.output_dir)
            except pyppeteer.errors.PageError as e:
                print(f'[screenshotghoul - ERR] failed to screenshot domain \
                     {url}: {e}')

            final_results.append({
                "domain": url,
                "contentghoul_result": content_result,
                "fingerghoul_result": finger_result,
                "gapihunter_result": gapi_result
            })

    else:
        url = args.domain
        content_result = contentghoul.scan_domain(url)
        if content_result["can_resolve"] is False:
            output_results(final_results, args.teams_webhook)
            return

        finger_result = fingerghoul.scan_domain(url)
        gapi_result = gapihunter.check_url(url)

        screenshotghoul.run_take_screenshot(url, page, '.')

        final_results.append({
            "domain": url,
            "contentghoul_result": content_result,
            "fingerghoul_result": finger_result,
            "gapihunter_result": gapi_result
        })
    output_results(final_results, args.teams_webhook)


if __name__ == "__main__":
    main()
