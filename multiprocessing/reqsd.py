import collections
import datetime
import random
import signal
import sys
import threading
import time


class CircularCounter():
    def __init__(self):
        self.lock = threading.RLock()
        self.n = 3600
        self.counters = collections.deque(maxlen=self.n)
        for _ in xrange(self.n):
            self.counters.append(0)
        self.reqs = 0.0
        self.reqm = 0.0
        self.reqh = 0.0
        self.last = CircularCounter._epoch()

    @staticmethod
    def _epoch():
        return int(time.time())

    def stats(self):
        epoch = CircularCounter._epoch()
        now = datetime.datetime.fromtimestamp(epoch).strftime("%Y-%m-%d %H:%M:%S")
        with self.lock:
            self.add(epoch, True)
            print "%s: (%d, %d, %.8f, %.8f) " % (now, epoch, self.reqs, self.reqm, self.reqh)

    def add(self, epoch = None, ignore = False):
        if epoch is None:
            epoch = CircularCounter._epoch()
        elif epoch < self.last:
            raise ValueError("invalid epoch {0} (must be >= {1})".format(epoch, self.last))
        with self.lock:
            self.reqs = self.counters[0]
            self.reqm = sum(list(self.counters)[0:60]) / 60.0
            self.reqh = sum(self.counters) / 3600.0
            delta = epoch - self.last
            self.last = epoch
            if delta >= self.n:
                delta = self.n
            for _ in xrange(delta):
                self.counters.appendleft(0)
            if not ignore:
                self.counters[0] += 1


class Runner(threading.Thread):
    def __init__(self, cc):
        threading.Thread.__init__(self)
        self.cc = cc

    def run(self):
        while True:
            time.sleep(random.randint(1,5))
            self.cc.add()


class Stats(threading.Thread):
    def __init__(self, cc):
        threading.Thread.__init__(self)
        self.cc = cc

    def run(self):
        while True:
            time.sleep(1)
            self.cc.stats()


def sigterm_handler(signo, _):
    print "Ctrl+C %(sig)d captured..." % {'sig': signo}
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)

    random.seed()

    c = CircularCounter()

    l = [Runner(c) for x in range(100)]
    l.append(Stats(c))

    for r in l:
        r.setDaemon(True)
        r.start()

    try:
        for r in l:
            while r.is_alive(): r.join(1)
    except (KeyboardInterrupt, SystemExit) as err:
        sigterm_handler(signal.SIGTERM, None)

    sys.exit(0)
