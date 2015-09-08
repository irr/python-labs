#!/usr/bin/env python
import argparse
import logging.handlers
import multiprocessing
import os
import signal
import subprocess
import sys

LOG_LEVEL = logging.INFO
LOG_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'

SYSLOG = logging.handlers.SysLogHandler(address='/dev/log')
SYSLOG.setFormatter(logging.Formatter(LOG_FORMAT))

PYTHON = "%s/%s" % (os.getcwd(), "web.py")
BINARY = PYTHON.split(".py")[0]

PIDS = set()


def pkill():
    for pid in PIDS:
        logging.getLogger().info('Killing process {p}...'.format(p=pid))
        os.kill(pid, signal.SIGTERM)
    wait_for_all()


def sigterm_handler(sig, _):
    if sig == signal.SIGTERM:
        pkill()
    sys.exit(0)


def wait_for_all():
    try:
        while PIDS:
            pid, retval = os.wait()
            logging.getLogger().info('Process {p} finished {r}'.format(p=pid, r=retval))
            PIDS.remove(pid)
    except (KeyboardInterrupt, SystemExit):
        pkill()


if __name__ == "__main__":
    logging.basicConfig(format=LOG_FORMAT)
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-s', '--syslog',
                        dest="syslog",
                        action='store_true',
                        help="enable syslog (default: disabled)")
    PARSER.add_argument('-b', '--bind',
                        dest="bind",
                        default="0.0.0.0",
                        help="bind address (default: 0.0.0.0)")
    PARSER.add_argument('-p', '--port',
                        dest="port",
                        type=int,
                        default=8000,
                        help="listen port (default: 8000)")
    PARSER.add_argument('-i', '--intances',
                        dest="instances",
                        type=int,
                        default=0,
                        help="instances number (supervisor only, default:<cpu-count>)")

    ARGS = PARSER.parse_args()

    if ARGS.syslog:
        logging.getLogger().addHandler(SYSLOG)

    logging.getLogger().setLevel(LOG_LEVEL)

    signal.signal(signal.SIGTERM, sigterm_handler)

    sys.argv[0] = BINARY
    if not os.path.isfile(BINARY):
        sys.argv[0] = PYTHON

    pids = set()

    if ARGS.instances <= 0:
        ARGS.instances = multiprocessing.cpu_count()

    logging.getLogger().info('Using {p} workers'.format(p=ARGS.instances))

    port = ARGS.port

    if "-p" not in sys.argv and "--port" not in sys.argv:
        sys.argv.append("-p")
        sys.argv.append(str(port))

    for instance in range(ARGS.instances):
        args = []
        for n, arg in enumerate(sys.argv):
            if n > 0 and args[n - 1] in ["-p", "--port"]:
                args.append(str(port))
                port += 1
            else:
                args.append(arg)
        process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE)
        logging.getLogger().info('Process {p} started'.format(p=process.pid))
        PIDS.add(process.pid)

    wait_for_all()
