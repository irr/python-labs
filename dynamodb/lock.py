import boto3
import decimal
import time

from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('prd')

now = int(time.time())

expiration_secs = 5

try:
    res = table.update_item(
        Key={"h": "irrlab", "r": "lock"},
        UpdateExpression="set c = :val",
        ExpressionAttributeValues={":val": decimal.Decimal(now + expiration_secs), ":cond": decimal.Decimal(now)},
        ConditionExpression="c < :cond",
        ReturnValues="UPDATED_NEW"
    )
    print(res)
except ClientError as e:
    print("locked!", e.__class__.__name__ == "ConditionalCheckFailedException")

"""
(venv) [irocha@irrlab dynamodb (master)]$ python lock.py ; sleep 3; python lock.py; sleep 2; python lock.py
{'Attributes': {'c': Decimal('1548307599')}, 'ResponseMetadata': {'RequestId': 'GJJSE9JLEIPKPIMRC438JHOLDRVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Thu, 24 Jan 2019 05:26:35 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '39', 'connection': 'keep-alive', 'x-amzn-requestid': 'GJJSE9JLEIPKPIMRC438JHOLDRVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '144160330'}, 'RetryAttempts': 0}}
locked! True
{'Attributes': {'c': Decimal('1548307606')}, 'ResponseMetadata': {'RequestId': 'SRRUGIQCG464G9761EBJNS6MRBVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Thu, 24 Jan 2019 05:26:41 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '39', 'connection': 'keep-alive', 'x-amzn-requestid': 'SRRUGIQCG464G9761EBJNS6MRBVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '2619370190'}, 'RetryAttempts': 0}}
(venv) [irocha@irrlab dynamodb (master)]$ python lock.py; sleep 3; python lock.py; sleep 2; python lock.py; sleep 1; python lock.py
{'Attributes': {'c': Decimal('1548307623')}, 'ResponseMetadata': {'RequestId': '8ES3MLVMTQN2TMDBPQGQEHSEVBVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Thu, 24 Jan 2019 05:26:59 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '39', 'connection': 'keep-alive', 'x-amzn-requestid': '8ES3MLVMTQN2TMDBPQGQEHSEVBVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '419972277'}, 'RetryAttempts': 0}}
locked! True
{'Attributes': {'c': Decimal('1548307630')}, 'ResponseMetadata': {'RequestId': 'GRPLAOF2S1NQVOARH2AA2DC6VJVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Thu, 24 Jan 2019 05:27:06 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '39', 'connection': 'keep-alive', 'x-amzn-requestid': 'GRPLAOF2S1NQVOARH2AA2DC6VJVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '2515856832'}, 'RetryAttempts': 0}}
locked! True
"""
