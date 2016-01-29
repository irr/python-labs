import random, signal, sys, time, threading

class Producer(threading.Thread):
    """
    Produces random integers to a list
    """

    def __init__(self, integers, condition):
        """
        Constructor.

        @param integers list of integers
        @param condition condition synchronization object
        """
        threading.Thread.__init__(self)
        self.integers = integers
        self.condition = condition

    def run(self):
        """
        Thread run method. Append random integers to the integers list
        at random time.
        """
        while True:
            integer = random.randint(0, 256)
            self.condition.acquire()
            print 'condition acquired by %s' % self.name
            self.integers.append(integer)
            print '%d appended to list by %s' % (integer, self.name)
            print 'condition notified by %s' % self.name
            self.condition.notify()
            print 'condition released by %s' % self.name
            self.condition.release()
            time.sleep(1)

class Consumer(threading.Thread):
    """
    Consumes random integers from a list
    """

    def __init__(self, integers, condition):
        """
        Constructor.

        @param integers list of integers
        @param condition condition synchronization object
        """
        threading.Thread.__init__(self)
        self.integers = integers
        self.condition = condition

    def run(self):
        """
        Thread run method. Consumes integers from list
        """
        while True:
            self.condition.acquire()
            print 'condition acquired by %s' % self.name
            while True:
                if self.integers:
                    integer = self.integers.pop()
                    print '%d popped from list by %s' % (integer, self.name)
                    break
                print 'condition wait by %s' % self.name
                self.condition.wait()
            print 'condition released by %s' % self.name
            self.condition.release()


def sigterm_handler(signo, _):
    print "Ctrl+C (%d) captured..." % (signo,)
    sys.exit(0)

def main():
    signal.signal(signal.SIGTERM, sigterm_handler)

    integers = []
    condition = threading.Condition()
    t1 = Producer(integers, condition)
    t2 = Consumer(integers, condition)
    t1.setDaemon(True)
    t2.setDaemon(True)
    t1.start()
    t2.start()

    try:
        while t1.is_alive():
            t1.join(1)
        while t2.is_alive():
            t2.join(1)
    except (KeyboardInterrupt, SystemExit) as err:
        sigterm_handler(signal.SIGTERM, None)

if __name__ == '__main__':
    main()
