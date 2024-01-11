#! /usr/bin/env python3

from screenshotghoul import screenshotghoul
from contentghoul import contentghoul
from fingerghoul import fingerghoul
from nrdghoul import nrdghoul

from pyppeteer import launch
import pyppeteer
import argparse
import requests
import asyncio
import json
import os

from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def main():
    parser = argparse.ArgumentParser(prog='ghoulhunter', description='hunt for phishing sites')
    parser.add_argument('--brand-keywords', '-k', nargs='+', help='regex expression keywords')
    parser.add_argument('--domain', '-d', help="Point ghoulhunter at a specific domain")
    parser.add_argument('--output-dir', '-o', help="Output directory", default="output/")
    parser.add_argument('--time', '-t', help="Days back", default=1, type=int)
    parser.add_argument('--chrome-path', '-c', help="Path to chrome executable", default="/sbin/google-chrome-stable")
    parser.add_argument('--screenshot', '-s', help="Only screenshot domains", action=argparse.BooleanOptionalAction)
    parser.add_argument('--input-file', '-i', help="Input domains from a file", type=str)
    args = parser.parse_args()

    print(f"[ghoulhunter - INFO] starting ghoulhunter with args: {args}")
    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)
    
    async def get_browser():
        browser = await launch({"args": ['--disable-gpu', '--disable-dev-shm-usage'], "executablePath": args.chrome_path})
        page = await browser.newPage()
        page.setDefaultNavigationTimeout(5000)
        return page
    page = asyncio.get_event_loop().run_until_complete(get_browser())
    
    final_results = []

    if args.screenshot and args.domain is None:
        results = nrdghoul.scan(args.brand_keywords, args.time, args.input_file)
        for url in results:
            try:
                print(f'[screenshotghoul - INFO] screenshotting {url}')
                screenshotghoul.run_take_screenshot(url, page, args.output_dir)
            except pyppeteer.errors.PageError as e:
                print(f'[screenshotghoul - ERR] failed to screenshot domain {url}: {e}')
    elif args.domain is None:
        results = nrdghoul.scan(args.brand_keywords, args.time, args.input_file)
        for url in results:
            content_result = contentghoul.scan_domain(url)
            if content_result["can_resolve"] is False:
                continue

            finger_result = fingerghoul.scan_domain(url)

            screenshotghoul.run_take_screenshot(url, page, args.output_dir)

            final_results.append({"domain": url, "contentghoul_result": content_result, "fingerghoul_result": finger_result})

    else:
        url = args.domain
        content_result = contentghoul.scan_domain(url)
        if content_result["can_resolve"] is False:
            print(json.dumps(final_results, indent=2))
            return

        finger_result = fingerghoul.scan_domain(url)

        screenshotghoul.run_take_screenshot(url, page, '.')

        final_results.append({"domain": url, "contentghoul_result": content_result, "fingerghoul_result": finger_result})
    print(json.dumps(final_results, indent=2))


if __name__ == "__main__":
    main()
