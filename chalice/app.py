from chalice import Chalice, Response

import json

app = Chalice(app_name='chapp')

@app.route('/')
def index():
    return Response(body=json.dumps(app.current_request.to_dict()),
                    status_code=200,
                    headers={'Content-Type': 'application/json'})

"""

aws apigateway update-rest-api --rest-api-id 2mk0o5c691 --patch-operations op=replace,path=/minimumCompressionSize,value='0'

(dev3) [irocha@irrlab chalice (master)]$ aws apigateway create-deployment --rest-api-id 2mk0o5c691 --region us-east-1 --stage-name api
{
    "id": "tdsrc8",
    "createdDate": 1525785583
}
(dev3) [irocha@irrlab chalice (master)]$ aws apigateway update-stage --region us-east-1 --rest-api-id 2mk0o5c691 --stage-name api --patch-operations op='replace',path='/deploymentId',value='tdsrc8'
{
    "deploymentId": "tdsrc8",
    "stageName": "api",
    "cacheClusterEnabled": false,
    "cacheClusterStatus": "NOT_AVAILABLE",
    "methodSettings": {},
    "createdDate": 1525785504,
    "lastUpdatedDate": 1525785624
}

(dev3) [irocha@irrlab chalice (master)]$ aws apigateway get-deployments --rest-api-id 2mk0o5c691 --region us-east-1
{
    "items": [
        {
            "id": "ach8yw",
            "createdDate": 1525785504
        },
        {
            "id": "tdsrc8",
            "createdDate": 1525785583
        }
    ]
}

aws apigateway get-deployments --rest-api-id 2mk0o5c691 --region us-east-1

aws apigateway delete-deployment --rest-api-id 2mk0o5c691 --deployment-id ach8yw --region us-east-1

http -v https://2mk0o5c691.execute-api.us-east-1.amazonaws.com/api/

"""