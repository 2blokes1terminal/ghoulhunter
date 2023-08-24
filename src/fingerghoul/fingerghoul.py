fingerprints = {
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
                "value": "http://2m.ma"
                "is_pos": False,
            },
            {
                "key": "Location",
                "value": "./index.html"
                "is_pos": False,
            }
        ],
        "paths": [
            {
                "path": "/prohqcker.php",
                "code": 302,
                "is_pos": True,
            },
            {
                "path": "/MyGov.zip",
                "code": 200,
                "is_pos": False
            },
            {
                "path": "/config.php",
                "code": 200,
                "is_pos": False
            }
        ]
    }
}
