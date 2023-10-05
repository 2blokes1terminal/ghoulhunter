from fingerghoul.fingerprints import fingerprints

import requests
import re

def check_header(header, res_headers):
    header_key = re.compile(header["key"], re.IGNORECASE)
    header_value = re.compile(header["value"], re.IGNORECASE)

    for res_header in res_headers.keys():
        if header_key.search(res_header.lower()) is not None:
            if header_value.search(res_headers[res_header]) is not None:
                return True

    return False

def check_path(domain, path):
    return False

def scan_domain(domain):
    print(f"[fingerghoul - INFO] fingerprinting {domain}")

    matched = []
    for fingerprint_name in fingerprints.keys():
        finger_total = 0
        finger_matched = 0
        finger_pos = False
        fingerprint = fingerprints[fingerprint_name]
        print(f"[fingerghoul - INFO] trying fingerprint {fingerprint_name}")

        for ua in fingerprint["meta"]["useragents"]:
            headers = {
                "User-Agent": ua #fingerprint["meta"]["useragents"][0]
            }
            try:
                req = requests.get(f"https://{domain}/", headers=headers, verify=False)
            except requests.exceptions.ConnectionError:
                return []

            # HEADER CHECK
            for header in fingerprint["headers"]:
                if check_header(header, req.headers):
                    print(f"[fingerghoul - INFO]\tHEADER MATCH: {header}")

                    if header["is_pos"]:
                        finger_pos = True
                    finger_matched += 1
                    finger_total += 1
                else:
                    finger_total += 1

            # PATH CHECK
            for path in fingerprint["paths"]:
                req_path = path["path"]
                codes = path["code"]
                content_re = [re.compile(cre, re.IGNORECASE) for cre in path["content"]]

                print(f"[fingerghoul - DEBUG] fingerprinting path {req_path}")
                
                req = requests.get(f"https://{domain}{req_path}", headers=headers, verify=False)
                for cre in content_re:
                    if re.search(cre, req.text) is not None:
                        print(f"[fingerghoul - INFO\tCONTENT MATCH: {cre}]")
                        if path["is_pos"]:
                            finger_pos = True
                        finger_matched += 1
                        finger_total += 1
                    else:
                        finger_total += 1

                for code in codes:
                    if code == req.status_code:
                        print(f"[fingerghoul - INFO\tSTATUS MATCH: {code}]")
                        # if path["is_pos"]:
                        #     finger_pos = True
                        finger_matched += 1
                        finger_total += 1
                    else:
                        finger_total += 1


        matched.append({"name": fingerprint_name, "matches": finger_matched, "total": finger_total, "positive": finger_pos})

    return matched
