import grequests

urls = [
    'http://www.heroku.com',
    'http://tablib.org',
    'http://httpbin.org',
    'http://python-requests.org',
    'http://kennethreitz.com'
]

rs = (grequests.get(u) for u in urls)

m = grequests.map(rs)

print m

