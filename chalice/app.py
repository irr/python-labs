from chalice import Chalice, Response

import json

app = Chalice(app_name='chapp')

@app.route('/')
def index():
    return Response(body=json.dumps(app.current_request.to_dict()),
                    status_code=200,
                    headers={'Content-Type': 'application/json'})

"""

aws apigateway update-rest-api --rest-api-id 2zwhyrcycf --patch-operations op=replace,path=/minimumCompressionSize,value='0'

http -v https://2zwhyrcycf.execute-api.us-east-1.amazonaws.com/api/

"""