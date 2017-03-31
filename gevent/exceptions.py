import gevent
from gevent import monkey
monkey.patch_all()


def worker(n):
    if not (n % 2):
        print('ok', n)
    else:
        raise ValueError("n error = {}".format(n))

def exception_callback(g):
    print('exception', g.exception)


if __name__=='__main__':
    jobs = []
    for n in range(7):
        job = gevent.spawn(worker, n)
        job.link_exception(exception_callback)
        jobs.append(job)
    gevent.joinall(jobs)

