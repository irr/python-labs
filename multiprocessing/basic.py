import multiprocessing
import time
import random

COUNT = 0

def worker(n):
    global COUNT
    """worker function"""
    for x in range(5):
        print('Worker {}'.format(n), COUNT)
        COUNT = COUNT + 1
        time.sleep(random.random())
    return

if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = multiprocessing.Process(target=worker, args=(i,))
        jobs.append(p)
        p.start()

print('Exit')
