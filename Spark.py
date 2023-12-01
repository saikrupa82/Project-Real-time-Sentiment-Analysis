from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType

def create_spark_session(app_name):
    return SparkSession.builder.appName(app_name).getOrCreate()

def read_kafka_stream(spark, bootstrap_servers, api_key, api_secret, topic):
    return spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", bootstrap_servers) \
        .option("kafka.sasl.jaas.config", f"org.apache.kafka.common.security.plain.PlainLoginModule required username='{api_key}' password='{api_secret}';") \
        .option("kafka.security.protocol", "SASL_SSL") \
        .option("kafka.sasl.mechanism", "PLAIN") \
        .option("subscribe", topic) \
        .load()

def main():
    spark = create_spark_session("ConfluentSparkExample")
    kafka_bootstrap_servers = "pkc-4r087.us-west2.gcp.confluent.cloud:9092"
    kafka_api_key = "JJXL2EA33YM35TUX"
    kafka_api_secret = "CKKN1U2re/0Q2AVSwA+ObPFfUW81dMqSLKvyWIg3VjtNsNaOwFMxUXN6aBToAdxi"
    kafka_topic = "twitter"

    df = read_kafka_stream(spark, kafka_bootstrap_servers, kafka_api_key, kafka_api_secret, kafka_topic)

    # Define schema for the Kafka message value (assuming it's in JSON format)
    schema = StructType([StructField("message", StringType(), True)])
    
    # Parse the JSON message and select the "message" field
    parsed_df = df.selectExpr("CAST(value AS STRING) as json_message") \
                  .select(from_json("json_message", schema).alias("data")) \
                  .select("data.message")

    # Your processing logic here
    # For example, you can perform transformations, aggregations, or write to another sink

    query = parsed_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()
