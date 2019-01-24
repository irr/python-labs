import boto3
import decimal
import time
import sys

from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ncds-db')

now = int(time.time())

expiration_secs = 5

try:
    res = table.put_item(
        Item={"k": "irrlab2", "t": decimal.Decimal(now + expiration_secs)},
        ConditionExpression="attribute_not_exists(k)",
        ReturnValues="NONE"
    )
    print(f"now={now}, exp={expiration_secs}", res)
except ClientError as e:
    try:
        res = table.update_item(
            Key={"k": "irrlab2"},
            UpdateExpression="set t = :val",
            ExpressionAttributeValues={":val": decimal.Decimal(now + expiration_secs), ":cond": decimal.Decimal(now)},
            ConditionExpression="t < :cond",
            ReturnValues="UPDATED_NEW"
        )
        print(f"now={now}, exp={expiration_secs}", res)
    except ClientError as e:
        print(f"now={now}, exp={expiration_secs} locked!", e.__class__.__name__ == "ConditionalCheckFailedException")

"""
now=1548308211, exp=5 {'Attributes': {'c': Decimal('1548308216')}, 'ResponseMetadata': {'RequestId': 'T47Q58T4REEVNOEP5Q2OR7H7ARVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Thu, 24 Jan 2019 05:36:52 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '39', 'connection': 'keep-alive', 'x-amzn-requestid': 'T47Q58T4REEVNOEP5Q2OR7H7ARVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '2048102356'}, 'RetryAttempts': 0}}
now=1548308215, exp=5 locked! True
now=1548308218, exp=5 {'Attributes': {'c': Decimal('1548308223')}, 'ResponseMetadata': {'RequestId': 'HICH3HG1D7MAQCDRP94D7U3AKFVV4KQNSO5AEMVJF66Q9ASUAAJG', 'HTTPStatusCode': 200, 'HTTPHeaders': {'server': 'Server', 'date': 'Thu, 24 Jan 2019 05:36:59 GMT', 'content-type': 'application/x-amz-json-1.0', 'content-length': '39', 'connection': 'keep-alive', 'x-amzn-requestid': 'HICH3HG1D7MAQCDRP94D7U3AKFVV4KQNSO5AEMVJF66Q9ASUAAJG', 'x-amz-crc32': '879194634'}, 'RetryAttempts': 0}}
now=1548308221, exp=5 locked! True
"""
