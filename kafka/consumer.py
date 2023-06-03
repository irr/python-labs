from kafka import KafkaConsumer
from kafka import TopicPartition

import time, sys

TOPIC = 'irrlab'
RESET = True

N = 1

# Create a Kafka consumer with the desired configuration
consumer = KafkaConsumer(
    group_id='irrlab-group-3',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda x: x.decode('utf-8'))

# Get the list of partitions for the topic
partitions = consumer.partitions_for_topic(TOPIC)

# Create a list of TopicPartition objects for the topic's partitions
topic_partitions = [TopicPartition(TOPIC, p) for p in partitions]

# Expliciting assigning instead of using the constructor
consumer.assign(topic_partitions)

if RESET:
    # Seek to offset 0 for all partitions
    for tp in topic_partitions:
        consumer.seek(tp, 0)
            
while True:
    messages = consumer.poll(timeout_ms=5000)
    for topic_partition, messages in messages.items():
        for message in messages:
            print(f"{N:3} Partition: {message.partition}, Offset: {message.offset}, Value: {message.value}")
            N = N + 1
