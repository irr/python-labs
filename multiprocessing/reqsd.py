import collections
import datetime
import random
import signal
import sys
import threading
import time


class CircularCounter():
    def __init__(self):
        self.lock = threading.Lock()
        self.n = 3600
        self.counters = collections.deque(maxlen=self.n)
        for _ in xrange(self.n):
            self.counters.append(0)
        self.reqs = 0.0
        self.reqm = 0.0
        self.last = int(time.time())

    def stats(self):
        ts = int(time.time())
        now = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        with self.lock:
            data = (ts, self.reqs, self.reqm, self.reqh)
            print "%s: %s" % (now, data)

    def touch(self, t):
        with self.lock:
            self.reqs = self.counters[0]
            self.reqm = sum(list(self.counters)[0:60]) / 60.0
            self.reqh = sum(self.counters) / 3600.0
            delta = t - self.last
            self.last = t
            for _ in xrange(delta):
                self.counters.appendleft(0)
            self.counters[0] += 1
            self.stats()


class Runner(threading.Thread):
    def __init__(self, cc):
        threading.Thread.__init__(self)
        self.cc = cc

    def run(self):
        while True:
            time.sleep(random.randint(1,5))
            self.cc.touch(int(time.time()))


def sigterm_handler(signo, _):
    print "Ctrl+C (%d) captured..." % (signo,)
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)

    random.seed()

    c = CircularCounter()

    l = [Runner(c) for x in range(100)]
    for r in l:
        r.setDaemon(True)
        r.start()

    try:
        for r in l:
            while r.is_alive(): r.join(1)
    except (KeyboardInterrupt, SystemExit) as err:
        sigterm_handler(signal.SIGTERM, None)

    sys.exit(0)
