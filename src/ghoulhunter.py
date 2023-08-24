#! /usr/bin/env python3

from scanner import scanner

import argparse

def main():
    parser = argparse.ArgumentParser(prog='ghoulhunter', description='hunt for phishing sites')

    parser.add_argument('--brand-keywords', '-k', nargs='+', help='regex expression keywords', required=True)

    args = parser.parse_args()

    results = scanner.scan(args.brand_keywords)
    print("\n".join(results))

if __name__ == "__main__":
    main()
