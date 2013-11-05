from __future__ import with_statement

from eventlet.green import urllib2
import eventlet
import re

# http://daringfireball.net/2009/11/liberal_regex_for_matching_urls
url_regex = re.compile(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))')


def fetch(url, outq):
    """Fetch a url and push any urls found into a queue."""
    print "fetching", url
    data = ''
    with eventlet.Timeout(5, False):
        data = urllib2.urlopen(url).read()
    for url_match in url_regex.finditer(data):
        new_url = url_match.group(0)
        outq.put(new_url)

            
def producer(start_url):
    """Recursively crawl starting from *start_url*.  Returns a set of 
    urls that were found."""
    pool = eventlet.GreenPool()
    seen = set()
    q = eventlet.Queue()
    q.put(start_url)
    # keep looping if there are new urls, or workers that may produce more urls
    while not q.empty() or pool.running() != 0:
        url = eventlet.with_timeout(0.1, q.get, timeout_value='')
        # limit requests to eventlet.net so we don't crash all over the internet
        if url not in seen and 'eventlet.net' in url:
            seen.add(url)
            pool.spawn_n(fetch, url, q)
    return seen


seen = producer("http://eventlet.net")
print "I saw these urls:"
print "\n".join(seen)
