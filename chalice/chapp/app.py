from chalice import Chalice

import requests
import time

app = Chalice(app_name='chapp')

@app.route('/v1/test/{t}')
def index(t):
    s = int(t)
    if s > 0:
        time.sleep(s)
    r = requests.get("https://www.google.com/")
    return {"pause": (s > 0), "elapsed": t, "status": r.status_code}
