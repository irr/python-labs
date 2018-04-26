from chalice import Chalice, Response

import json
import requests
import time

app = Chalice(app_name='chapp')
app.debug = True

@app.route('/v1/test/{t}')
def index(t):
    s = int(t)
    if s > 0:
        time.sleep(s)
    r = requests.get("https://www.google.com/")
    response = {"v": "r2", "pause": (s > 0), "elapsed": t, "status": r.status_code, "request": app.current_request.to_dict()}
    return Response(body=json.dumps(response),
                    status_code=200,
                    headers={'Content-Type': 'application/json'})

"""

aws apigateway update-rest-api --rest-api-id cjs6q30umi --patch-operations op=replace,path=/minimumCompressionSize,value='0'

http -v https://cjs6q30umi.execute-api.us-east-1.amazonaws.com/api/v1/test/0

http -v https://cjs6q30umi.execute-api.us-east-1.amazonaws.com/api/v1/test/0|head -21

http -v https://cjs6q30umi.execute-api.us-east-1.amazonaws.com/api/v1/test/0 User-Agent:"Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"|head -21

"""