from datetime import datetime

from airflow.sdk import dag, task


@dag(
    dag_id="hello_world",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["test"],
)
def hello_world():

    @task
    def say_hello():
        print("Hello from Airflow in Docker!")
        return "done"

    @task
    def say_goodbye(previous):
        print(f"The previous task returned: {previous}")

    say_goodbye(say_hello())


hello_world()