import requests

def resolve_url(base_url):
    r = requests.get(base_url)
    return r.url

if __name__ == '__main__':
    import sys
    print(resolve_url(sys.argv[1]))

