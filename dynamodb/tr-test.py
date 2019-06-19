import boto3

client = boto3.client('dynamodb')

items = [{
    "Update": {
        "TableName": "test",
        "Key": { "h": { "S": f"h{n}" }, "r": { "S": f"r{n}" } },
        "ConditionExpression": "attribute_not_exists(h)",
        "UpdateExpression": "set t = :element",
        "ExpressionAttributeValues": { ":element": { "S": f"{n * 100}" } },
        "ReturnValuesOnConditionCheckFailure": "ALL_OLD"
    }
} for n in range(10)]

response = client.transact_write_items(TransactItems=items)

print(response)

