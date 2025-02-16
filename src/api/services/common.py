from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from confluent_kafka import Producer, KafkaError
import json
import os
import logging
import datetime

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Custom Exception Classes ---
class DatabaseError(Exception):
    pass

class AgentNotFoundError(Exception):
    pass

class KafkaPublishError(Exception):
    pass

# --- Kafka Producer Configuration ---
kafka_conf = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
    'client.id': 'trading-bot-api'
}
producer = Producer(kafka_conf)

# --- CORS Configuration ---
origins = [
    "http://localhost:3000",  # Frontend URL
]

def setup_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# --- Helper Functions ---
def publish_event(topic, event_type, data: dict):
    event = {
        "event_type": event_type,
        "timestamp": str(datetime.datetime.now()),
        "data": data
    }
    try:
      producer.produce(topic, json.dumps(event).encode('utf-8'))
      producer.flush()
    except KafkaError as e:
        logger.error(f"Kafka error: {e}")
        raise KafkaPublishError(f"Failed to publish event to Kafka: {e}")