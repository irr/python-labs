from gevent.pywsgi import WSGIServer
from cgi import parse_qs, escape

import argparse, gevent, json, logging, logging.handlers

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'

SYSLOG = logging.handlers.SysLogHandler(address='/dev/log')
SYSLOG.setFormatter(logging.Formatter(LOG_FORMAT))

logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(LOG_LEVEL)

def application(environ, start_response):
    status = '200 OK'
    headers = [('Content-Type', 'application/json; charset=utf-8')]

    start_response(status, headers)
    yield "%s\n" % json.dumps({"bind": args.bind, "port": args.port})[:1024]

global args

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--syslog', 
                        dest="syslog", 
                        action='store_true', 
                        help="enable syslog (default: disabled)")
    parser.add_argument('-b', '--bind', 
                        dest="bind", 
                        default="0.0.0.0",
                        help="bind address (default: 0.0.0.0)")
    parser.add_argument('-p', '--port', 
                        dest="port", 
                        type=int,
                        default=8000,
                        help="listen port (default: 8000)")
    args = parser.parse_args()
    if args.syslog:
        logging.getLogger().addHandler(SYSLOG)
    logging.info('Listening on %s:%d...' % (args.bind, args.port))
    WSGIServer((args.bind, args.port), application).serve_forever()
