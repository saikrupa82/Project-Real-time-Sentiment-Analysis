import json
import pandas as pd
from time import sleep
from kafka import KafkaProducer

#initialise the kafka producer object
kafka_producer = KafkaProducer(bootstrap_servers = ['localhost:9092'],  \
                value_serializer = lambda x:json.dumps(x).encode('utf-8'))

#read the data from csv file and convert to list of dictionaries
Tweets_dataframe = pd.read_csv('Tweets.csv')
Tweets = Tweets_dataframe.to_json(orient = 'records')
Tweets_records=json.loads(Tweets)

#iterating over list of dictionaries and sending each record to Kafka Cluster 
for Tweet in Tweets:
    print(Tweet)
    kafka_producer.send('Twitter', value = Tweet)
    sleep(1)