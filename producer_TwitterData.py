import csv
import json
import time
from confluent_kafka import Producer

# Constants
CSV_FILE_PATH = 'Tweets.csv'
KAFKA_TOPIC = 'Twitter'
CONFIG_FILE = './client.properties'

# Function to read configuration for Confluent Cloud
def load_kafka_config(filename):
    config = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                config[key] = value.strip()
    return config

# Kafka Producer setup
producer = Producer(load_kafka_config(CONFIG_FILE))

# Function to publish message to Kafka
def publish_message(producer, topic, message):
    producer.produce(topic, value=json.dumps(message))
    producer.flush()

# Function to process and send tweets from CSV to Kafka
def send_tweets_to_kafka(file_path, topic):
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            data = {
                'Sno': row['Sno'],
                'Datetime': row['Datetime'],
                'TweetId': row['Tweet Id'],
                'Text': row['Text'],
                'Username': row['Username'],
                'Sentiment': row['sentiment'],
                'SentimentScore': row['sentiment_score'],
                'Emotion': row['emotion'],
                'EmotionScore': row['emotion_score']
            }
            publish_message(producer, topic, data)
            time.sleep(2)  # Wait for 2 seconds

# Main function
def main():
    send_tweets_to_kafka(CSV_FILE_PATH, KAFKA_TOPIC)

if __name__ == '__main__':
    main()
