from urllib import request


def fetch(url: str):
    req = request.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) '
                   'AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 '
                   'Mobile/10A5376e Safari/8536.25')
    return request.urlopen(req).read().decode('utf-8')
