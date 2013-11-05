import sys

from urllib import urlencode
from urllib2 import URLError, HTTPError, urlopen
from json import loads

# python /home/irocha/python/wsgi/test.py

try:
    url = 'http://localhost:8888/map?' + urlencode({'u':'admin','j':'all'})
    res = urlopen(url, timeout=5).read()
    print loads(res)
except HTTPError as he:
    print he.code
except URLError as ue:
    print str(ue)
except:
    print "Exception: ", str(sys.exc_info())

