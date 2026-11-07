from datetime import datetime

from airflow.sdk import dag, task


@dag(
    dag_id="spark_test",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["test"],
)
def spark_test():

    @task.bash
    def run_spark_job():
        return "spark-submit --master 'local[*]' /opt/airflow/spark/jobs/test_job.py"

    run_spark_job()


spark_test()