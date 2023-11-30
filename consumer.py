import re
import findspark
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, udf
from pyspark.sql.types import StructType, StructField, StringType, ArrayType

if __name__ == "__main__":
    findspark.init()

    # Path to the pre-trained model
    path_to_model = './pre_trained_model'

    # Config
    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .appName("TwitterSentimentAnalysis") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2") \
        .getOrCreate()

    # Spark Context
    sc = spark.sparkContext
    sc.setLogLevel('ERROR')

    # Schema for the incoming data
    schema = StructType([StructField("message", StringType())])

    # Read the data from Kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "twitter") \
        .option("startingOffsets", "latest") \
        .option("header", "true") \
        .load() \
        .selectExpr("CAST(value AS STRING) as message")

    df = df.withColumn("value", from_json("message", schema))

    # Pre-processing the data
    pre_process = udf(
        lambda x: re.sub(r'[^A-Za-z\n ]|(http\S+)|(www.\S+)', '', x.lower().strip()).split(), ArrayType(StringType())
    )
    df = df.withColumn("cleaned_data", pre_process(df.message)).dropna()

    # Load the pre-trained model
    try:
        pipeline_model = PipelineModel.load(path_to_model)
    except Exception as e:
        print(f"Error loading the model: {e}")
        spark.stop()
        exit(1)

    # Make predictions
    prediction = pipeline_model.transform(df)

    # Select the columns of interest
    prediction = prediction.select(prediction.message, prediction.prediction)

    # Print prediction in the console
    query = prediction \
        .writeStream \
        .format("console") \
        .outputMode("update") \
        .start()

    # Await termination of the streaming query
    try:
        query.awaitTermination()
    except KeyboardInterrupt:
        print("Termination signal received. Stopping the streaming query.")
        query.stop()
    finally:
        # Stop the Spark session gracefully
        spark.stop()
