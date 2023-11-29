import csv
from kafka import KafkaProducer
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO)

# Kafka Producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic_name = 'twitter'  # Modify according to your topic name

# Function to send data to Kafka
def send_to_kafka(tweet_text):
    data = {
        'message': tweet_text.replace(',', '')
    }
    producer.send(topic_name, value=json.dumps(data).encode('utf-8'))

# Function to read tweets from CSV and send to Kafka
def process_tweets(csv_file):
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tweet_text = row['tweet_text']  # Change 'tweet_text' to the name of your column
            send_to_kafka(tweet_text)
            logging.info(f"Sent tweet: {tweet_text}")

# Main execution
if __name__ == '__main__':
    csv_file_path = 'Tweets.csv'  # Specify the path to your CSV file
    process_tweets(csv_file_path)
