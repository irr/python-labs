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
        self.lock = threading.Lock()
        self.n = 60
        self.idx = 0
        self.counters = array('i', [0 for _ in range(self.n)])

    def touch(self):
        with self.lock:
            self.counters[self.idx] += 1

    def run(self):
        while True:
            time.sleep(1)
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with self.lock:
                print "%s => (%02d) req/s = %d" % (now, self.idx, self.counters[self.idx])
                self.idx = (self.idx + 1) % self.n
                if self.idx == 0:
                    s = sum(self.counters)
                    print "\t%s => (%d) req/m = %f" % (now, s, s / float(self.n))
                self.counters[self.idx] = 0


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
