from airflow.sdk import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

import os
from datetime import  timedelta
from pendulum import datetime

airflow_home = os.getenv("AIRFLOW_HOME", "/opt/bitnami/airflow")


# Create the DAG
with DAG("weekly_summary_dag",
            start_date=datetime(2025, 5, 23, tz='local'),
            schedule="@weekly",
            catchup=False,
            tags=["summary","knowledge_graph","portfolio","news"],
            default_args={
                "owner": "airflow",
                "start_date": datetime(2025, 5, 23, tz='local'),
                "retries": 3,
                "retry_delay": timedelta(minutes=5),
            },
            ) as dag:
            

            create_table_task = SQLExecuteQueryOperator(
                task_id="create_fitness_table_if_not_exists",
                conn_id="postgres_default",
                sql="""
                    CREATE TABLE IF NOT EXISTS weekly_summaries (
                                    id SERIAL PRIMARY KEY,
                                    week_start DATE NOT NULL,
                                    week_end DATE NOT NULL,
                                    summary_text TEXT,
                                    topic_model JSONB,
                                    created_at TIMESTAMP DEFAULT now()
                                );""",
            )

            create_network_table_task = SQLExecuteQueryOperator(
                task_id="create_network_metrics_table_if_not_exists",
                conn_id="postgres_default",
                sql="""
                    CREATE TABLE IF NOT EXISTS network_metrics (
                        id SERIAL PRIMARY KEY,
                        week_start DATE,
                        num_nodes INTEGER,
                        num_edges INTEGER,
                        avg_path_length FLOAT,
                        clustering_coefficient FLOAT,
                        num_communities INTEGER,
                        created_at TIMESTAMP DEFAULT now()
                    );
                    """,
            )

            create_node_table_task = SQLExecuteQueryOperator(
                task_id="create_node_metrics_table_if_not_exists",
                conn_id="postgres_default",
                sql="""
                    CREATE TABLE IF NOT EXISTS node_metrics (
                        id SERIAL PRIMARY KEY,
                        week_start DATE,
                        metrics JSONB,
                        created_at TIMESTAMP DEFAULT now()
                    );
                    """,
            )


            run_summarization_and_topic = SparkSubmitOperator(
                task_id="run_summarization",
                application= airflow_home + "/spark_jobs/run_summarization_and_topic.py",
                jars=airflow_home + "/spark_jobs/jars/postgresql-42.2.5.jar",
                conn_id="spark_default",
            )

            build_graph_task = SparkSubmitOperator(
                task_id="build_kg",
                application= airflow_home + "/spark_jobs/build_KG.py",
                jars=airflow_home + "/spark_jobs/jars/postgresql-42.2.5.jar",
                conn_id="spark_default",
            )
        

            create_table_task >> create_node_table_task >> create_network_table_task >> run_summarization_and_topic >> build_graph_task
