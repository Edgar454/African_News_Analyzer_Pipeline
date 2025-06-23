import os
import json
import datetime
from pyspark.sql.types import *


def save_node_metrics_spark(spark, metrics: dict, week_start: str, connection_properties: dict, jdbc_url: str):

    node_metrics = json.dumps(metrics["top_nodes"])

    schema = StructType([
        StructField("week_start", DateType(), True),
        StructField("metrics", StringType(), True),  # JSONB is just a string to Spark
        StructField("created_at", TimestampType(), True),
    ])

    # Prepare a list of one dict for single-row DataFrame
    row_data = [{
        "week_start": week_start,
        "metrics": node_metrics,
        "created_at": datetime.datetime.now()
    }]

    # Convert to Spark DataFrame
    df = spark.createDataFrame(row_data , schema=schema)

    # Write to PostgreSQL
    df.write \
      .format("jdbc") \
      .option("url", jdbc_url) \
      .option("dbtable", "node_metrics") \
      .options(**connection_properties) \
      .mode("append") \
      .save()

    print("Node metrics saved")


    

def save_network_metrics_spark(spark, metrics: dict, week_start: str, connection_properties: dict, jdbc_url: str):
    global_metrics = metrics["global"]

    # Prepare a list of one dict for single-row DataFrame
    row_data = [{
        "week_start": week_start,
        "num_nodes": global_metrics["nodes"],
        "num_edges": global_metrics["edges"],
        "avg_path_length": global_metrics["average_path_length"],
        "clustering_coefficient": global_metrics["global_clustering_coefficient"],
        "num_communities": global_metrics["communities"],
        "created_at": datetime.datetime.now()
    }]
    
    schema = StructType([
                    StructField("week_start", DateType(), True),
                    StructField("num_nodes", IntegerType(), True),
                    StructField("num_edges", IntegerType(), True),
                    StructField("avg_path_length", DoubleType(), True),
                    StructField("clustering_coefficient", DoubleType(), True),
                    StructField("num_communities", IntegerType(), True),
                    StructField("created_at", TimestampType(), True)
                ])

    # Convert to Spark DataFrame
    df = spark.createDataFrame(row_data , schema=schema)

    # Write to PostgreSQL
    df.write \
      .format("jdbc") \
      .option("url", jdbc_url) \
      .option("dbtable", "network_metrics") \
      .options(**connection_properties) \
      .mode("append") \
      .save()

    print("Network metrics saved")