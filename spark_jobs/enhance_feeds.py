from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, concat_ws, regexp_replace , to_timestamp
from pyspark.sql.types import StructType, StringType , ArrayType
from dotenv import load_dotenv
import os

print("Started the Enhancing script")
load_dotenv()

NEWS_TOPIC = os.getenv("KAFKA_NEWS_TOPIC", "news_topic")
KAFKA_HOST = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
POSTGRES_SERVER = os.environ.get("POSTGRES_SERVER", "172.27.176.1")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "postgres")

spark = SparkSession.builder \
    .appName("RSS Stream Processor") \
    .getOrCreate()

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_HOST) \
    .option("subscribe", NEWS_TOPIC) \
    .option("failOnDataLoss", "false") \
    .option("kafka.security.protocol", "PLAINTEXT") \
    .load()

df_parsed = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

schema = StructType() \
    .add("title", StringType()) \
    .add("link", StringType()) \
    .add("author", StringType()) \
    .add("description", StringType()) \
    .add("pubDate", StringType()) \
    .add("content", StringType()) \
    .add("tags", ArrayType(StringType()))

df_json = df_parsed.withColumn("data", from_json(col("value"), schema)).select("data.*")
df_json = df_json.withColumnRenamed("pubDate", "published_date")

# Define the format pattern matching your input string
df_json = df_json.withColumn(
    "published_date",
    regexp_replace("published_date", "^[A-Za-z]{3}, ", "")
)

df_json = df_json.withColumn("published_date",
                   regexp_replace(col("published_date"), "GMT", "+0000"))

date_format_pattern_cleaned = "dd MMM yyyy HH:mm:ss Z"

# Convert the cleaned string to timestamp and overwrite the 'published_date' column
df_json = df_json.withColumn(
    "published_date",
    to_timestamp(df_json["published_date"], date_format_pattern_cleaned)
)

def escape_quotes_in_string_columns(df):
    for column_name, dtype in df.dtypes:
        if dtype == "string":
            df = df.withColumn(column_name, regexp_replace(col(column_name), '"', '""'))
    return df

df_escaped = escape_quotes_in_string_columns(df_json)

# PostgreSQL connection parameters
jdbc_url = f"jdbc:postgresql://{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}?stringtype=unspecified"
connection_properties = {
        "user": os.environ.get("POSTGRES_USER"),
        "password": os.environ.get("POSTGRES_PASSWORD"),
        "driver": "org.postgresql.Driver"
    }


def write_to_postgres(batch_df, batch_id):
    if batch_df.isEmpty():
        return

    # Read existing keys from Postgres
    existing_keys_df = spark.read \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", "(SELECT title, published_date FROM news) AS existing") \
        .options(**connection_properties) \
        .load()

    # Filter out existing entries
    filtered_batch = batch_df.join(
        existing_keys_df,
        on=["title", "published_date"],
        how="left_anti"
    )

    # Write only new entries
    filtered_batch.write \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", "news") \
        .options(**connection_properties) \
        .mode("append") \
        .save()



query = df_escaped.writeStream \
    .foreachBatch(write_to_postgres) \
    .outputMode("append") \
    .option("checkpointLocation", "data/checkpoints/postgres") \
    .start()


query.awaitTermination()
