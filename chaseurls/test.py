import requests

def chase_redirects(url):
    while True:
        yield url
        r = requests.head(url)
        if 300 < r.status_code < 400:
            url = r.headers['location']
        else:
            print(r.status_code)
            break

if __name__ == '__main__':
    import sys
    for url in chase_redirects(sys.argv[1]):
        print(url)
