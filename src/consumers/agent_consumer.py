from confluent_kafka import Consumer, KafkaError
import json
import os
from dotenv import load_dotenv
from src.data.agent_dao import create_agent, update_agent, delete_agent
import asyncio

load_dotenv()

# --- Kafka Consumer Configuration ---
kafka_conf = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
    'group.id': 'agent-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(kafka_conf)
consumer.subscribe(['agents'])

async def process_event(event):
    """Processes a single Kafka event."""
    try:
        if event['event_type'] == 'agent.created':
            await create_agent(event['data'])
            print(f"Agent created: {event['data']['id']}")
        elif event['event_type'] == 'agent.updated':
            await update_agent(event['data']['id'], event['data'])
            print(f"Agent updated: {event['data']['id']}")
        elif event['event_type'] == 'agent.deleted':
            await delete_agent(event['data']['id'])
            print(f"Agent deleted: {event['data']['id']}")
        else:
            print(f"Unknown event type: {event['event_type']}")
    except Exception as e:
        print(f"Error processing event: {e}")

async def consume_events():
    """Consumes Kafka events and processes them."""
    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print('Reached end of partition')
                elif msg.error():
                    raise KafkaError(msg.error())
            else:
                event = json.loads(msg.value().decode('utf-8'))
                await process_event(event)

    except KeyboardInterrupt:
        print('Interrupted. Closing consumer...')
    finally:
        consumer.close()

if __name__ == '__main__':
    asyncio.run(consume_events())