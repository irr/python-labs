import asyncio
import concurrent.futures
import boto3
from timeit import default_timer as timer

# Replace with your own AWS profile
session = boto3.Session(profile_name="default")
regions = ["us-east-1", "us-east-2", "us-west-1", "us-west-2", "eu-west-1", "eu-west-2", "eu-west-3"]

async def non_blocking(executor):
    loop = asyncio.get_event_loop()
    blocking_tasks = []
    for region in regions:
        ec2_client = session.client("ec2", region_name=region)
        blocking_tasks.append(loop.run_in_executor(executor, ec2_client.describe_instances))
    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]
    return results

def blocking():
    results = []
    for region in regions:
        ec2_client = session.client("ec2", region_name=region)
        results.append(ec2_client.describe_instances())
    return results        


if __name__ == '__main__':
    executor = concurrent.futures.ThreadPoolExecutor(
        max_workers=10,
    )
    event_loop = asyncio.get_event_loop()

    # blocking first
    start = timer()
    blocking_results = blocking()
    elapsed = (timer() - start)
    print("Blocking took: {}".format(elapsed))

    # async next
    start = timer()
    non_blocking_results = event_loop.run_until_complete(non_blocking(executor))
    elapsed = (timer() - start)
    print("Non-blocking took: {}".format(elapsed))
