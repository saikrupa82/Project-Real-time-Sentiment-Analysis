import six
import sys
from kafka import KafkaConsumer

# Workaround for six.moves issue with kafka-python on Python 3.12
if sys.version_info >= (3, 12):
    sys.modules['kafka.vendor.six.moves'] = six.moves

# Kafka configuration
bootstrap_servers = ['localhost:9092']
topic_name = 'Twitter'

# Create a Kafka consumer
consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=bootstrap_servers,
    auto_offset_reset='earliest',
    group_id='my-group',
    enable_auto_commit=True,
    value_deserializer=lambda x: x.decode('utf-8')
)

# Process messages
for message in consumer:
    print(f"Received message: {message.value}")
    # Here you can add your logic to process message
