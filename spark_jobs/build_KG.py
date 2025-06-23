import os
import datetime
from utils.processing_utils import build_and_save_knowledge_graph
from utils.date_utils import get_week_range
from utils.spark_utils import save_network_metrics_spark , save_node_metrics_spark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col


def run_build_knowledge_graph():
    spark = SparkSession.builder \
    .appName("Knowledge graph building Job") \
    .getOrCreate()

    # PostgreSQL connection parameters
    jdbc_url = "jdbc:postgresql://172.27.176.1:5432/postgres?stringtype=unspecified"
    connection_properties = {
        "user": os.environ.get("POSTGRES_USER"),
        "password": os.environ.get("POSTGRES_PASSWORD"),
        "driver": "org.postgresql.Driver"
    }

    # Step 1: Read Spark DataFrame from Postgres
    df = spark.read.format("jdbc").options(
        url=jdbc_url,
        dbtable="news",
        **connection_properties
    ).load()

    # filter for only this week data
    week_start, week_end = get_week_range()
    week_df = df.filter((col("published_date") >= week_start) & (col("published_date") <= week_end))

    # Step 2: Convert to Pandas
    pandas_df = df.toPandas()

    # Step 3: Build and save knowledge graph
    knowledge_graph, metrics  = build_and_save_knowledge_graph(pandas_df)

    # Step 4: Save the network metrics to Postgres
    save_network_metrics_spark(spark, metrics, week_start, connection_properties, jdbc_url)

    # save the node metrics
    save_node_metrics_spark(spark, metrics, week_start, connection_properties, jdbc_url)

    spark.stop()
    
    return knowledge_graph

if __name__ == "__main__":
    run_build_knowledge_graph()
    print("Graph built and saved succesfully")