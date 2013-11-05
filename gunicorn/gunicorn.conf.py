# gunicorn -c gunicorn.conf.py --log-config logging-console.conf test:app 1>&2
# supervisord -c supervisord.conf 
# supervisorctl shutdown
# supervisorctl status
# supervisorctl start|stop|restart

import multiprocessing

bind = ":8080"
workers = multiprocessing.cpu_count() * 2 + 1
worker_connections = 1000
worker_class = "gevent"
backlog = 2048
max_requests = 0
timeout = 30
graceful_timeout = 30
keep_alive = 5
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
debug = True
spew = False
preload_app = False
daemon = False
user = "irocha"
group = None
umask = 0
pidfile = None
check_config = False
pythonpath = "/home/irocha/git/python-labs/gunicorn/"

errorlog = '-'
loglevel = 'debug'
accesslog = '-'

def on_starting(server):
    pass

def on_reload(server):
    pass

def when_ready(server):
    pass

def pre_fork(server, worker):
    pass

def post_fork(server, worker):
    pass

def pre_exec(server):
    pass

def pre_request(worker, req):
    #worker.log.debug("%s %s" % (req.method, req.path))
    pass

def post_request(worker, req, environ):
    pass

def worker_exit(server, worker):
    pass

                                
