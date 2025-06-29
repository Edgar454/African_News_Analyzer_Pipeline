import os
import json
import datetime
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from utils.date_utils import get_week_range
from utils.processing_utils import perform_summary, perform_topic_modeling 
load_dotenv()

POSTGRES_SERVER = os.environ.get("POSTGRES_SERVER", "172.27.176.1")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "postgres")

def run_summarization_and_topic_modeling():
    spark = SparkSession.builder \
    .appName("Topic Modeling and Summarization Job") \
    .getOrCreate()

    # PostgreSQL connection parameters
    jdbc_url = f"jdbc:postgresql://{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}?stringtype=unspecified"
    connection_properties = {
        "user": os.environ.get("POSTGRES_USER"),
        "password": os.environ.get("POSTGRES_PASSWORD"),
        "driver": "org.postgresql.Driver"
    }

    # Step 1: Get the week range for the current week
    start_date, end_date = get_week_range()


    # Step 1: Read Spark DataFrame from Postgres
    df = spark.read.format("jdbc").options(
        url=jdbc_url,
        dbtable="news",
        **connection_properties
    ).load()

    week_df = df.filter((col("published_date") >= start_date) & (col("published_date") <= end_date))

    # Perform summarization
    print("Starting Summarization")
    week_pandas_df = week_df.toPandas()
    summary = perform_summary(week_pandas_df)
    print("Summarization Ended Sucessfully")


    # Perform topic modeling
    print("Starting Topic Modeling")
    topics_data , vectorizer, lda , doc_term_matrix = perform_topic_modeling(week_pandas_df)
    print("Modeling Ended Successfuly")

    # Serialize topic output (assuming it's a list of topic strings or dicts)
    topics_json = json.dumps(topics_data)


    # Create a single-row dictionary
    summary_data = [{
        "week_start": start_date,
        "week_end": end_date,
        "summary_text": summary,
        "topic_model": topics_json,
        "created_at": datetime.datetime.now()
    }]

    # Convert to Spark DataFrame
    summary_df = spark.createDataFrame(summary_data)

    summary_df.write.format("jdbc").options(
        url=jdbc_url,
        dbtable="weekly_summaries",
        **connection_properties
    ).mode("append").save()


if __name__ == "__main__":
    run_summarization_and_topic_modeling()
    print("Sumarization executed successfuly")


    
    