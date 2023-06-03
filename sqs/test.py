import boto3
import os
import concurrent.futures
import threading

QUEUE_URL = os.environ.get('UPLOAD_QUEUE_URL')

print(QUEUE_URL)

sqs = boto3.client('sqs', region_name='eu-west-1')

def process_task(message, receipt_handle):
    # your code for processing SQS message comes here
    print(f"SQS message from {threading.get_native_id()}", message)
    delete_sqs_message(receipt_handle)

def delete_sqs_message(receipt_handle):
    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=QUEUE_URL,
        ReceiptHandle=receipt_handle
    )

if __name__ == "__main__":
    def get_message():
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10,
        )

        if len(response.get('Messages', [])) > 0:
            messages = response.get("Messages", [])
            message = messages[0]
            return message
        else:
            return None
    
    num_threads = 4
    with concurrent.futures.ThreadPoolExecutor(num_threads) as executor:
        futures = []
        while True:
            if len(futures) < num_threads:
                message = get_message()
                if message is not None:
                    request = message['Body']
                    future = executor.submit(process_task, request, message['ReceiptHandle'])
                    futures.append(future)
            else:
                done, futures = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)
                futures = list(futures)
