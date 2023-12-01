from confluent_kafka import Consumer
import json
import os

def read_ccloud_config(config_file):
    conf = {}
    with open(config_file) as fh:
        for line in fh:
            line = line.strip()
            print("line : " + line)
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                conf[parameter] = value.strip()
    print("Running spark application")
    print(conf)
    return conf


props = read_ccloud_config("./client.properties")
props["group.id"] = "python-group-1"
props["auto.offset.reset"] = "earliest"

consumer = Consumer(props)
consumer.subscribe(["twitter"])

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
                print("Received JSON Message:")
                print("Key:", key)
                print("Value:", json_data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")

except KeyboardInterrupt:
    pass
finally:
    consumer.close()