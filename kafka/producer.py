import random
from kafka import KafkaProducer

# Set up the Kafka producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# Number of messages to send
N = 1

# Send N random messages to the topic
for i in range(N):
    # Generate a random message
    message = str(random.random())

    # Send the message to the topic
    producer.send('irrlab', message.encode())

# Flush the producer to ensure all messages are sent
producer.flush()
