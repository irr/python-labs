# python -B Server.py --help
# python -B Server.py --logging=debug

# http localhost:8888/
# http localhost:8888/static/index.html

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado import gen
from tornado.options import define, options

import momoko, os, sys, signal, time, logging, traceback

from handlers import *

define("config", help="config file", default=None, type=str)
define("address", help="binding host", default="localhost", type=str)
define("port", help="binding port", default=8888, type=int)

define("db_host", help="database host", default="localhost", type=str)
define("db_port", help="database port", default=5432, type=int)
define("db_database", help="database name", default="stock", type=str)
define("db_user", help="database user", default="psql", type=str)
define("db_password", help="database password", default="psql", type=str)
define("db_min_conn", help="minimum amount of connections", default=1, type=int)
define("db_max_conn", help="maximum amount of connections", default=10, type=int)
define("db_cleanup_timeout", help="time in seconds between pool cleanups", default=10, type=int)


def shutdown():
    io_loop = tornado.ioloop.IOLoop.instance()
    if io_loop.running():
        io_loop.stop()
    logging.getLogger().info("server stopped")


def on_signal(sig, frame):
    if http_server != None:
        logging.getLogger().info("shutting down server...")
        http_server.stop()
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def main():
    global http_server

    try:
        signal.signal(signal.SIGTERM, on_signal)
        
        tornado.options.parse_command_line()
        if options.config != None:
            tornado.options.parse_config_file(options.config)

        path = os.path.join(os.path.dirname(__file__), "templates")

        application = tornado.web.Application([
            (r'/', OverviewHandler),
            (r'/dynamic', DynamicOverviewHandler, dict(template_path=path)),
            (r'/query', SingleQueryHandler),
            (r'/batch', BatchQueryHandler),
            (r'/chain', QueryChainHandler),
            (r'/multi_query', MultiQueryHandler),
            (r'/callback_and_wait', CallbackWaitHandler)], 
            template_path=path, 
            static_path=os.path.join(os.path.dirname(__file__), "static"), 
            debug=True)

        application.db = momoko.AsyncClient({
            'host': options.db_host,
            'port': options.db_port,
            'database': options.db_database,
            'user': options.db_user,
            'password': options.db_password,
            'min_conn': options.db_min_conn,
            'max_conn': options.db_max_conn,
            'cleanup_timeout': options.db_cleanup_timeout
        })

        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(options.port, options.address)
        logging.getLogger().info("server listening on port %s:%d" % 
            (options.address, options.port))
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.getLogger().debug("autoreload enabled")
            tornado.autoreload.start()        
        tornado.ioloop.IOLoop.instance().start()

    except KeyboardInterrupt:
        logging.getLogger().info("exiting...")

    except BaseException as ex:
        logging.getLogger().error("exiting due: [%s][%s]" % 
            (str(ex), str(traceback.format_exc().splitlines())))
        sys.exit(1)


if __name__ == '__main__':
    main()
