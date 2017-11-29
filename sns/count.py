import arrow
import boto3
import json

client = boto3.client('sns')


def get_topic_arn(topic):
    global client

    arn = None
    nt = ""
    arns = {}

    while True:
        result = client.list_topics(NextToken=nt)
        index = { topic["TopicArn"].split(":")[-1]: topic["TopicArn"] for topic in result.get("Topics", [])}
        arns = { **index, **arns }
        nt = result.get("NextToken", "")
        if nt is "":
            break

    return arns.get(topic, None)


def count(topic):
    global client

    now = arrow.utcnow().float_timestamp
    total = 0
    topic = get_topic_arn(topic)
    if topic is None:
         return {"total": total, "timespent": arrow.utcnow().float_timestamp - now}

    nt = ""
    while True:
        subs = client.list_subscriptions_by_topic(TopicArn=topic, NextToken=nt)
        total += len(subs.get("Subscriptions", 0))
        nt = subs.get("NextToken", "")
        if nt is "":
            break

    return {"total": total, "timespent": arrow.utcnow().float_timestamp - now}
