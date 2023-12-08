import json
import time
from confluent_kafka import Consumer, Producer
from textblob import TextBlob

def load_kafka_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                config[key] = value.strip()
    return config

def analyze_sentiment(text):
    return TextBlob(text).sentiment

def find_competitors(text, competitor_set):
    found_competitors = [comp for comp in competitor_set if comp.lower() in text.lower()]
    return found_competitors

def extract_competitor_names(text):
    return {word for word in text.split() if word.startswith('@')}

def create_producer(config_path):
    producer_config = load_kafka_config(config_path)
    return Producer(producer_config)

def send_to_kafka_with_wait(producer, topic, key, value, wait_time=3):
    if key is not None:
        key = key.encode('utf-8')
    value = json.dumps(value).encode('utf-8')
    producer.produce(topic, key=key, value=value)
    producer.flush()
    print(f"Sent data to Kafka:\nKey: {key}\nValue: {value}")
    time.sleep(wait_time)  # Introduce a 3-second wait time

def main():
    consumer_config = load_kafka_config("./client.properties")
    consumer_config.update({"group.id": "python-group-1", "auto.offset.reset": "earliest"})

    producer_config_path = "./client_writeback.properties"  # Path to producer config
    output_topic = "Write_Back_Data"  # Kafka topic to send data to

    competitors = set()  # Initialize an empty set to hold competitor names

    consumer = Consumer(consumer_config)
    producer = create_producer(producer_config_path)  # Create a Kafka producer

    consumer.subscribe(["Twitter"])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is not None and msg.error() is None:
                key = msg.key().decode('utf-8') if msg.key() else None
                value = json.loads(msg.value().decode('utf-8'))

                text = value.get('Text', '').strip()

                print(f"Received JSON Message:\nKey: {key}\nValue: {value}")

                sentiment = analyze_sentiment(text)
                print(f"Sentiment Analysis: Polarity={sentiment.polarity}, Subjectivity={sentiment.subjectivity}")

                competitors.update(extract_competitor_names(text))
                competitors_found = find_competitors(text, competitors)

                processed_data = {
                    "original_message": value,
                    "sentiment": {
                        "polarity": sentiment.polarity,
                        "subjectivity": sentiment.subjectivity
                    },
                    "competitors_mentioned": list(competitors_found)
                }

                # Send processed data to Kafka with a 3-second wait time
                send_to_kafka_with_wait(producer, output_topic, key, processed_data, wait_time=3)

    except KeyboardInterrupt:
        print("Stopped by user")
    finally:
        consumer.close()
        producer.flush()

if __name__ == '__main__':
    main()
