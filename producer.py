from datetime import datetime
from confluent_kafka import Producer
import pandas as pd
import json
import time
import random, csv

# Path to the CSV file
csv_path_file = 'Tweets.csv'
chunk_size = 100

# Function to read Confluent Cloud configuration
def read_ccloud_config(config_file):
    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                conf[parameter] = value.strip()
    return conf

# Function to generate random interval within a 5-minute window
def get_random_interval():
    return random.uniform(0, 30)

# Initialize Kafka producer
producer = Producer(read_ccloud_config("client.properties"))

# Function to send data to Kafka
def send_to_kafka(tweet_text):
    data = {
        'message': tweet_text.replace(',', '')
    }
    producer.produce(topic_name, value=json.dumps(data).encode('utf-8'))

# Function to process tweets from a CSV file
def process_tweets(csv_file_path):
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tweet_text = row['airline_sentiment']  # Change 'tweet_text' to the name of your column
            send_to_kafka(tweet_text)
            # logging.info(f"Sent tweet: {tweet_text}")
            producer.flush()

# Main execution
if __name__ == '__main__':
    topic_name = 'twitter'  # Modify according to your topic name
    process_tweets(csv_path_file)
