import arrow
import boto3

client = boto3.client('sns')

nt = ""

now = arrow.utcnow().float_timestamp * 1000

while True:
    subs = client.list_subscriptions(NextToken=nt)
    nt = subs.get("NextToken", "")
    if nt is "":
        break
    print(len(subs["Subscriptions"]))

timespent = arrow.utcnow().float_timestamp * 1000 - now
print(timespent)
