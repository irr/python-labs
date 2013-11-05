#!/usr/bin/env python

import sys, os, signal, logging, logging.handlers

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape
import tornado.template
import tornado.autoreload
from tornado.options import define, options

from utils import *
from handlers import *

define("port", default=8888, type=int)
define("syslog", default=False, type=bool)

# curl -v http://localhost:8888/;echo
# python Web.py --logging=debug

class WebApplication(tornado.web.Application):
    def __init__(self, **kwargs):
        path = os.path.join(os.path.dirname(__file__), "templates")
        kwargs.update(dict(template=path))
        handlers = [(r"/", IndexHandler, kwargs)]
        settings = dict(static_path=path)
        tornado.web.Application.__init__(self, handlers, **settings)

def shutdown():
    io_loop = tornado.ioloop.IOLoop.instance()
    if io_loop.running():
        io_loop.stop()
    logger.info("server stopped")
    sys.exit(0)

def shutdown_poll():
    remaining = len(tornado.ioloop.IOLoop.instance()._handlers)
    logging.info("[%d] waiting on handlers (%d remaining)",
            tornado.process.task_id() or 0, remaining)
    if remaining == 1:
        shutdown()

def shutdown_hook(sig, frame):
    logger.info("shutting down server (gracefully)...")
    if http_server != None:
        http_server.stop()
    shutdown_poll()    

def main():
    global logger
    global http_server
    signal.signal(signal.SIGTERM, shutdown_hook)
    tornado.options.parse_command_line()
    logger = Logger(options.logging, options.syslog)
    logger.info('listening on port [%d]' % options.port)
    http_server = tornado.httpserver.HTTPServer(WebApplication(**dict(logger=logger)))
    http_server.listen(options.port)
    try:
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logger.debug("autoreload enabled")
            tornado.autoreload.start()
        tornado.ioloop.IOLoop.instance().start()
    except BaseException, ex:
        logger.error("exiting due: [%s]" % str(ex))

if __name__ == "__main__":
    main()
