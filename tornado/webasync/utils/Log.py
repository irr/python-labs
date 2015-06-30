"""
Log wrapper
"""
# Copyright (c) - UOL Inc,
# Todos os direitos reservados
#
# Este arquivo e uma propriedade confidencial do Universo Online Inc.
# Nenhuma parte do mesmo pode ser copiada, reproduzida, impressa ou
# transmitida por qualquer meio sem autorizacao expressa e por escrito
# de um representante legal do Universo Online Inc.
#
# All rights reserved
#
# This file is a confidential property of Universo Online Inc.
# No part of this file may be reproduced or copied in any form or by
# any means without written permisson from an authorized person from
# Universo Online Inc.
#
# Autor: Ivan Ribeiro Rocha
# Baseado em https://github.com/irr/python-labs/tree/master/tornado

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
        self.id = hex(thread.get_ident())

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