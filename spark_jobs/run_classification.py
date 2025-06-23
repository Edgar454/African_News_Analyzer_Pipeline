import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from utils.processing_utils import perform_classification

def run_classification():
    spark = SparkSession.builder \
    .appName("Classification Job") \
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

    #filter out the already classified entries
    df = df.filter(col("category").isNull())

    if not df.isEmpty():

        # Step 2: Convert to Pandas
        pandas_df = df.toPandas()

        # Step 3: Classify in batches (LLM API)
        classified_df = perform_classification(pandas_df)  # returns the same df with "category"

        # Step 4: Convert back to Spark
        df = spark.createDataFrame(classified_df)

        # Step 5: Write back to Postgres
        df.write.format("jdbc").options(
            url=jdbc_url,
            dbtable="news",
            **connection_properties
        ).mode("overwrite").save()
    
    else:
        print("Nothing to classify")

if __name__ == "__main__":
    run_classification()
    print("Classification executed successfuly")