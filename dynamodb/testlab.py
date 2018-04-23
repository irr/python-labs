import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('testlab')

#table.put_item(Item={"h": "irr", "r": "_", "c": 0})

table.update_item(
    Key={"h": "irr", "r": "_"},
    UpdateExpression="set c = c + :val",
    ExpressionAttributeValues={":val": decimal.Decimal(1), ":cond": decimal.Decimal(100)},
    ConditionExpression="c <= :cond",
    ReturnValues="UPDATED_NEW"
)

table.get_item(Key={"h":"irr","r":"_"})

table.query(KeyConditionExpression=Key("h").eq("irr"))

table.query(IndexName="r-h-index", KeyConditionExpression=Key("r").eq("_"), ReturnConsumedCapacity="INDEXES")

table.query(KeyConditionExpression=Key('h').eq("irr") & Key('r').begins_with('_'),
    ProjectionExpression='r,h,c',
    ConsistentRead=True,
    ReturnConsumedCapacity='TOTAL',
    ScanIndexForward=True, Limit=5)

# Get LastEvaluatedKey and use it as ExclusiveStartKey

table.query(KeyConditionExpression=Key('h').eq("irr") & Key('r').begins_with('_'),
    ProjectionExpression='r,h,c',
    ConsistentRead=True,
    ReturnConsumedCapacity='TOTAL',
    ScanIndexForward=True,
    ExclusiveStartKey={'h': 'irr', 'r': '_3'},
    Limit=5)

with table.batch_writer() as batch:
    for i in range(9):
        batch.delete_item(Key={'h': "irr", 'r': "_{}".format(i)})

with table.batch_writer() as batch:
    for i in range(9):
        batch.put_item(Item={"h": "irr", "r": "_{}".format(i), "c": 0})