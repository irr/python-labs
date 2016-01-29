import datetime
import random
import signal
import sys
import threading
import time

from array import *


class CircularCounter(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.lock = threading.RLock()
        self.n = 60
        self.idx = 0
        self.counters = array('i', [0 for _ in range(self.n)])
        self.reqs = 0.0
        self.reqm = 0.0

    def touch(self):
        with self.lock:
            self.counters[self.idx] += 1

    def stats(self):
        ts = int(time.time())
        now = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        with self.lock:
            data = (int(time.time()), self.idx, self.reqs, self.reqm)
            print "%s: %s" % (now, data)

    def run(self):
        while True:
            time.sleep(1)
            with self.lock:
                self.reqs = self.counters[self.idx]
                self.idx = (self.idx + 1) % self.n
                if self.idx == 0:
                    self.reqm = sum(self.counters) / float(self.n)
                self.counters[self.idx] = 0
                self.stats()


class Runner(threading.Thread):
    def __init__(self, cc):
        threading.Thread.__init__(self)
        self.cc = cc

    def run(self):
        while True:
            self.cc.touch()
            n = random.random()
            time.sleep(n * 10)


def sigterm_handler(signo, _):
    print "Ctrl+C (%d) captured..." % (signo,)
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)

    random.seed()

    c = CircularCounter()
    c.setDaemon(True)
    c.start()

    l = [Runner(c) for x in range(1000)]
    for r in l:
        r.setDaemon(True)
        r.start()

    try:
        while c.is_alive(): c.join(1)
    except (KeyboardInterrupt, SystemExit) as err:
        sigterm_handler(signal.SIGTERM, None)

    sys.exit(0)
