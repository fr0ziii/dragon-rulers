from confluent_kafka import Consumer, KafkaError
import json
import os
from dotenv import load_dotenv
load_dotenv()

# --- Kafka Consumer Configuration ---
kafka_conf = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),  # Replace with your Kafka broker address
    'group.id': 'agent-consumer-group',
    'auto.offset.reset': 'earliest'  # Start reading from the beginning of the topic
}

consumer = Consumer(kafka_conf)

consumer.subscribe(['agents'])  # Subscribe to the 'agents' topic

try:
    while True:
        msg = consumer.poll(1.0)  # Poll for messages with a 1-second timeout

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                print('Reached end of partition')
            elif msg.error():
                raise KafkaError(msg.error())
        else:
            # Process the received message
            event = json.loads(msg.value().decode('utf-8'))
            if event['event_type'] == 'agent.created':
                print(f"Received agent.created event: {event}")
                # Add logic here to handle the agent.created event (e.g., store in database)

except KeyboardInterrupt:
    print('Interrupted. Closing consumer...')
finally:
    consumer.close()