fingerprints = {
    "parked": {
        "meta": {
            "useragents": [
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/118.0",
                "gh0ul",
            ]
        },
        "title": ".*&nbsp;-&nbsp;.*",
        "headers": [
            {
                "key": "x\-cache\-([a-zA-Z])+\-from",
                "value": "parking\-.*",
                "is_pos": True,
            }
        ],
        "paths": [
            {
                "path": "/",
                "code": [
                    200
                ],
                "content": [
                    ".*\>Sedo Domain Parking\<\/a\>.*"
                ],
                "is_pos": True
            },
            {
                "path": "/robots.txt",
                "code": [
                    200
                ],
                "content": [
                    "User-agent: Googlebot.*User-agent: Mediapartners-Google.*User-agent: Yahoo! Slurp"
                ],
                "is_pos": True,
            }
        ]
    },
    "cloudflare": {
        "meta": {
            "useragents": [
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/118.0",
                "gh0ul",
            ]
        },
        "title": "Just a moment...",
        "headers": [
            {
                "key": "server",
                "value": "cloudflare",
                "is_pos": True,
            }
        ],
        "paths": [
            {
                "path": "/",
                "code": [
                    403
                ],
                "content": [],
                "is_pos": True,
            }
        ]
    },
    "prohqcker": {
        "meta": {
            "useragents": [
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/118.0",
                "gh0ul",
                "curl/8.2.1",
            ]
        },
        "title": "Sign in with myGov - myGov",
        "headers": [
            {
                "key": "Location",
                "value": "http://2m.ma",
                "is_pos": False,
            },
            {
                "key": "Location",
                "value": "./index.html",
                "is_pos": False,
            }
        ],
        "paths": [
            {
                "path": "/prohqcker.php",
                "code": [
                    302,
                ],
                "content": [],
                "is_pos": True,
            },
            {  # other prohqcker actor using obfuscated js?
                "path": "/prohqcker.php",
                "code": [
                    503,
                    302
                ],
                "content": [
                    r"eval\((decodeURIComponent\(|escape\(|window\.atob\(){1,}?"
                ],
                "is_pos": True
            },
            {
                "path": "/MyGov.zip",
                "code": [
                    200
                ],
                "content": [],
                "is_pos": False
            },
            {
                "path": "/config.php",
                "code": [
                    200
                ],
                "content": [],
                "is_pos": False
            }
        ]
    }
}
