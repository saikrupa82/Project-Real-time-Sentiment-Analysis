from pyspark.sql import SparkSession
from pyspark.sql.streaming import *

spark = SparkSession \
    .builder \
    .appName("Spark Kafka Streaming") \
    .master("spark://172.18.0.10:7077") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0") \
    .getOrCreate()

# Configure Kafka bootstrap servers and subscribe to the topic
kafka_bootstrap_servers = "172.18.0.9:9092"
subscribe_topic = "test-topic"

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", subscribe_topic) \
    .option("startingOffsets", "earliest") \
    .load()

# Cast key and value to STRING
df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Define the Kafka producer options
kafka_producer_options = {
    "kafka.bootstrap.servers": "172.18.0.9:9092",
    "topic": "output-topic",  # Change this to your desired output topic
    "checkpointLocation": ""  # Change this to a directory on your system
}

# Write the output to the Kafka topic
query = df \
    .writeStream \
    .outputMode("update") \
    .format("kafka") \
    .options(**kafka_producer_options) \
    .start()

# Wait for the query to terminate
query.awaitTermination()
