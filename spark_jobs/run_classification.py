import os
import logging
from dotenv import load_dotenv
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import psycopg2
from utils.processing_utils import perform_classification

load_dotenv()

# Configure logging with timestamp
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

POSTGRES_SERVER = os.environ.get("POSTGRES_SERVER", "172.27.176.1")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "postgres")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

def run_classification():
    spark = SparkSession.builder.appName("Classification Job").getOrCreate()

    jdbc_url = f"jdbc:postgresql://{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}?stringtype=unspecified"
    connection_properties = {
        "user": POSTGRES_USER,
        "password": POSTGRES_PASSWORD,
        "driver": "org.postgresql.Driver"
    }

    df = spark.read.format("jdbc").options(
        url=jdbc_url,
        dbtable="news",
        **connection_properties
    ).load()

    df = df.filter(col("category").isNull()).select("id", "description")

    if df.rdd.isEmpty():
        logger.info("Nothing to classify")
        return

    pandas_df = df.toPandas()
    classified_df = perform_classification(pandas_df)  # adds 'category'

    classified_spark_df = spark.createDataFrame(classified_df).select("id", "category")

    staging_table = "news_staging"
    classified_spark_df.write.format("jdbc").options(
        url=jdbc_url,
        dbtable=staging_table,
        **connection_properties
    ).mode("overwrite").save()

    conn = psycopg2.connect(
        host=POSTGRES_SERVER,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE news AS n
            SET category = s.category
            FROM news_staging AS s
            WHERE n.id = s.id
        """)
        conn.commit()
    conn.close()

    logger.info("Classification update done.")

if __name__ == "__main__":
    run_classification()
    logger.info("Classification executed successfully")

