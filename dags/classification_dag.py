from airflow.sdk import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.providers.common.sql.sensors.sql import SqlSensor

import os
from datetime import  timedelta
from pendulum import datetime

spark_home = os.getenv("SPARK_JOBS_PARENT_FOLDER", "/opt/bitnami/airflow")


# Create the DAG
with DAG("Classification_dag",
            start_date=datetime(2025, 5, 23, tz='local'),
            schedule=None,
            catchup=False,
            tags=["classification","portfolio","news"],
            default_args={
                "owner": "airflow",
                "start_date": datetime(2025, 5, 23, tz='local'),
                "retries": 3,
                "retry_delay": timedelta(minutes=5),
            },
            ) as dag:


            wait_for_sql = SqlSensor(
                            task_id='wait_for_sql',
                            conn_id='postgres_default',
                            sql='SELECT COUNT(*) FROM news WHERE category IS NULL;',
                            success=lambda result: result > 0,
                            poke_interval=30,
                            timeout=600,
                            dag=dag,
                            )
            

        
            run_classification = SparkSubmitOperator(
                task_id="DataTransformation",
                application= spark_home + "/spark_jobs/run_classification.py",
                jars=spark_home + "/spark_jobs/jars/postgresql-42.2.5.jar",
                conn_id="spark_default",
            )

            wait_for_sql >> run_classification
