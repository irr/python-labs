import os, logging, thread
from logging.handlers import SysLogHandler

class Logger():
    def __init__(self, level, syslog = False):
        levels = {'critical': logging.CRITICAL,
                  'error': logging.ERROR,
                  'warning': logging.WARNING,
                  'info': logging.INFO,
                  'debug': logging.DEBUG}
        self.logger = logging.getLogger()
        self.logger.setLevel(levels.get(level))
        if syslog:
            for handler in self.logger.handlers:
                if isinstance(handler, logging.StreamHandler):
                    self.logger.removeHandler(handler)
            self.logger.addHandler(SysLogHandler(address='/dev/log'))
        self.id = hex(thread.get_ident())[2:]

    def fmt(self, msg):
        return "[%s] %s (%d)" % (self.id, msg, os.getpid())

    def debug(self, msg):
        self.logger.debug(self.fmt(msg))

    def info(self, msg):
        self.logger.info(self.fmt(msg))

    def warning(self, msg):
        self.logger.warning(self.fmt(msg))

    def error(self, msg):
        self.logger.error(self.fmt(msg))