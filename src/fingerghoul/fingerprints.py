fingerprints = {
    "parked": {
        "meta": {
            "useragents": [
                "gh0ul"
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
                ]
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
    "prohqcker": {
        "meta": {
            "useragents": [
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
                    302
                ],
                "content": [],
                "is_pos": True,
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
