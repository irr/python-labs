#!/home/irocha/dev/bin/python

import psutil
import time

chrome = { 'proc': None, 'zombie': False }

for proc in psutil.process_iter():
    try:
        if proc.name() == 'chrome':
            if proc.status() == psutil.STATUS_ZOMBIE:
                chrome['zombie'] = True
                print(proc, " zombie found.")
            if proc.ppid() == 1:
                chrome['proc'] = proc
                print(proc, " zombie (master) added.")
    except psutil.NoSuchProcess:
        pass


if chrome['zombie']:
    chrome['proc'].kill()
    print(chrome['proc'], " killed.")

