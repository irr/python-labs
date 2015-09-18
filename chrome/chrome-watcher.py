import logging.handlers
import psutil
import time

LOG_LEVEL = logging.INFO
LOG_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'

SYSLOG = logging.handlers.SysLogHandler(address='/dev/log')
SYSLOG.setFormatter(logging.Formatter(LOG_FORMAT))

logging.basicConfig(format=LOG_FORMAT)
logging.getLogger().setLevel(LOG_LEVEL)
logging.getLogger().addHandler(SYSLOG)

while not time.sleep(1):
    chrome = { 'proc': None, 'zombie': False }
    chromes = []

    for proc in psutil.process_iter():
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
        logging.getLogger().warn("killing zombie process: [%s]" % (chrome,))
        chrome['proc'].kill()
    elif len(chromes) == 1:
        logging.getLogger().warn("killing sleeping process: [%s]" % (chromes[0],))
        chromes[0].kill()

