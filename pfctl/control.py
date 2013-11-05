import sys
import requests

BASE = "http://192.168.56.2"

SESSION = requests.session()

def url(p):
    return BASE + p

def login(s):
    payload = {'usernamefld': 'admin', 'passwordfld': 'pfsense', 'login': 'Login'}
    r = s.post(url("/"), data=payload)
    if r.status_code == 302:
        r = s.get(url(r.headers['location']))
        print "logged in:", r.headers
        return (r, s)
    else:
        return (r, None)

if __name__ == '__main__':
    (r, s) = login(SESSION)
    if s == None:
        print "error logging in: (%d, %s)" % (r.status_code, r.headers)
        sys.exit(1)
