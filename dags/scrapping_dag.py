# add the parent folder to the file system to allow file importation
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from airflow.sdk import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime, timedelta
from kafka_producer.ingest_feed import ingest_feed

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 6, 22),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

urls = ['https://feeds.feedburner.com/AfricaIntelligence',
        'https://africapresse.com/feed/',]



with DAG(
    'scraping_dag',
    default_args=default_args,
    tags=["scrapping","portfolio","news"],
    description='A simple scraping DAG , that listen to rss feeds each 3 hours and store the data in a database',
    schedule=timedelta(hours=3) ) as dag:


        create_table_task = SQLExecuteQueryOperator(
                task_id="create_news_table_if_not_exists",
                conn_id="postgres_default",
                sql="""
                    CREATE TABLE IF NOT EXISTS news (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255),
                        link VARCHAR(255),
                        description TEXT,
                        published_date TIMESTAMP,
                        content TEXT,
                        tags TEXT[],
                        category VARCHAR(50),
                        author VARCHAR(100),
                        source VARCHAR(100),
                        UNIQUE (title, published_date)
                    );
                """,
            )

        scrape_task = PythonOperator(
            task_id='scrape_task',
            python_callable=ingest_feed,
            op_kwargs={
                'urls': urls
            },

        )

        trigger_next_dag = TriggerDagRunOperator(
            task_id='trigger_classification_dag',
            trigger_dag_id='Classification_dag',  
            wait_for_completion=False, 
            reset_dag_run=True,         
            trigger_rule=TriggerRule.ALL_SUCCESS, 
        )

        create_table_task >> scrape_task >> trigger_next_dag