from datetime import datetime
from termcolor import colored

import sys
import uuid

NAMESPACE = uuid.uuid4()
TOTAL = 3600 * 24 # day seconds
WINDOW = 10 * 60 # 10 minutes

now = datetime.utcnow()

def calculate(now):
    epoch = int(datetime(now.year, now.month, now.day, 0, 0).strftime('%s'))
    elapsed = int(now.timestamp()) - epoch
    slots = int(TOTAL / WINDOW)
    current_slot = int(elapsed / WINDOW) + 1
    print(f"{'current timestamp':>25}: {int(now.timestamp())}")
    print(colored(f"{'zero-hour timestamp':>25}: {epoch}", 'blue'))
    print(f"{'seconds per day':>25}: {TOTAL:>10}")
    print(f"{'elapsed seconds':>25}: {elapsed:>10}")
    print(colored(f"{'available slots':>25}: {slots:>10}", 'red'))
    print(colored(f"{'current slot':>25}: {current_slot:>10}", attrs=['bold']))
    token = uuid.uuid5(NAMESPACE, f"user1:user2:xxxxxxxx:{current_slot}")
    print(colored(f"{'x-gympass-idempotency-key':>25}: {token}", attrs=['bold']))


if __name__ == '__main__':
    now = datetime.utcnow()
    if len(sys.argv) != 2: 
        calculate(now)
    else:
        # python slots.py 18:47:14
        now = f"{now.year:04}-{now.month:02}-{now.day:02}T{sys.argv[1]}Z"
        date_time_obj = datetime.strptime(now, "%Y-%m-%dT%H:%M:%SZ")
        calculate(date_time_obj)

