try:
  import unzip_requirements
except ImportError:
  pass

import boto3
import datetime
import os
import simplejson as json


"""
sls create --template aws-python3 --path serverless
npm install --save-dev serverless-content-encoding
npm install serverless-offline --save-dev
sls plugin install -n serverless-python-requirements
"""

def _serialize(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError ("%s is not JSON serializable" % str(obj))


def hello(event, context):
    c = boto3.client('s3')

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event,
        "buckets": c.list_objects(Bucket="irrlab"),
        "env": os.environ["my_bucket"]
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body, ensure_ascii=False, default=_serialize)
    }

    return response
