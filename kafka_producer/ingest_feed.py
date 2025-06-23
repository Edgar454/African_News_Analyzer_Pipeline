import os
from confluent_kafka import Producer
import socket
from dotenv import load_dotenv
from kafka_producer.parser_utils import parse_multiple_feeds
load_dotenv()



def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Delivery failed for {msg.key()}: {err}")
    else:
        print(f"✅ Delivered {msg.key()} to {msg.topic()} [{msg.partition()}]")

def ingest_feed(urls):

    conf = {'bootstrap.servers': os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
        'client.id': socket.gethostname(),}
    producer = Producer(conf)
    NEWS_TOPIC = os.getenv("KAFKA_NEWS_TOPIC", "news_topic")

    parsed_feeds = parse_multiple_feeds(urls)
    
    for feed in parsed_feeds:
        if feed:
            try:
                print(f"Producing message for feed ID: {feed['id']}")
                producer.produce(NEWS_TOPIC, key=feed['id'], value=feed['content'])
            except Exception as e:
                print(f"Error producing message: {e}")

    producer.flush()

if __name__ == "__main__":
    # Example usage
    example_urls = [
        'https://feeds.feedburner.com/AfricaIntelligence',
        'https://africapresse.com/feed/',
    ]
    ingest_feed(example_urls)