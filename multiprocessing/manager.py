from multiprocessing import Process, Manager, current_process
import os, time, signal, sys

def f(d, l):
    def _sh(sig, _):
        if sig == signal.SIGTERM:
            print "_sh -> c: {0}, p: {1}".format(os.getpid(), os.getppid())
            sys.exit(0)

    signal.signal(signal.SIGTERM, _sh)

    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.reverse()
    print "f -> c: {0}, p: {1}".format(os.getpid(), os.getppid())
    try:
        while True:
            time.sleep(1000)
    finally:
        print "exiting..."


def main(d, l):
    print "main -> c: {0}, p: {1}".format(os.getpid(), os.getppid())
    p = Process(target=f, args=(d, l))
    p.start()
    p.join(2)
    p.terminate()

    print d
    print l


if __name__ == '__main__':
    manager = Manager()
    d = manager.dict()
    l = manager.list(range(10))

    main(d, l)
