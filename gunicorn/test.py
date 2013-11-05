import logging

log = logging.getLogger(__name__)

def app(environ, start_response):
    data = 'Test OK!\n'
    log.info("environ: %s" % environ)
    start_response('200 OK', [('Content-Type', 'text/plain'), 
                              ('Content-Length', str(len(data)))])
    yield data