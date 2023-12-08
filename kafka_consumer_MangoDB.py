from confluent_kafka import Consumer
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time  # Import the time module

# Function to read configuration for Kafka
def read_ccloud_config(config_file):
    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                conf[parameter] = value.strip()
    return conf

# MongoDB connection setup
uri = "mongodb+srv://gouravdeshmukh432:S6EAi9k3iEdgSqVd@twitter.z7dqigd.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
mydb = client['Twitter']
collection_name = mydb["Twitter_Collection"]

# Kafka Consumer setup
props = read_ccloud_config("./client_writeback.properties")
props["group.id"] = "python-group-1"
props["auto.offset.reset"] = "earliest"
consumer = Consumer(props)
consumer.subscribe(["Write_Back_Data"])

# Batch processing setup
batch_size = 100  # Number of messages per batch
batch = []
batch_count = 0

try:
    while True:
        msg = consumer.poll(1.0)
        if msg is not None and msg.error() is None:
            # Decode message key and value from bytes to string
            key = msg.key().decode('utf-8') if msg.key() else None
            val = msg.value().decode('utf-8') if msg.value() else None

            # Parse the JSON message
            try:
                json_data = json.loads(val)
                batch.append(json_data)
                batch_count += 1

                # Check if batch is ready to be written to MongoDB
                if batch_count >= batch_size:
                    # Insert batch into MongoDB
                    collection_name.insert_many(batch)
                    print(f"Batch of size {batch_count} inserted to MongoDB")

                    # Reset batch
                    batch = []
                    batch_count = 0

                # Add a 2-second wait
                time.sleep(2)

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

except KeyboardInterrupt:
    pass
finally:
    consumer.close()
    client.close()  
