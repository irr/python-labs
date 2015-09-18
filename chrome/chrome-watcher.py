import psutil
import time

while not time.sleep(0.5):
    chrome = { 'proc': None, 'zombie': False }
    chromes = []

    processes = [p for p in psutil.process_iter() if p.name() == 'chrome']

    for proc in processes:
        try:
            if proc.name() == 'chrome':
                if proc.status() == psutil.STATUS_ZOMBIE:
                    chrome['zombie'] = True
                if proc.ppid() == 1:
                    chrome['proc'] = proc
                chromes.append(proc)
        except psutil.NoSuchProcess:
            pass

    if chrome['zombie']:
        chrome['proc'].kill()
    elif len(chromes) == 1:
        chromes[0].kill()

