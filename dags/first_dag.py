from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Viktoras',
    'retries': 3,
    'retry_delay': timedelta(minutes=2)
}

with DAG(
    dag_id='first_dag_v2',
    default_args=default_args,
    description="Darome kazka",
    start_date=datetime(2023, 10, 12, 0),
    schedule_interval='@daily',
    catchup=False
) as dag:
    task1 = BashOperator(
        task_id='bash_operator',
        bash_command="echo Hello word, this is the first task."
    )

    task2 = BashOperator(
        task_id='bash_operator_2',
        bash_command="echo Hello word, this is the second task."
    )


    task3 = BashOperator(
        task_id='bash_operator_3',
        bash_command="echo Hello word, this is the third task."
    )

    task1 >> [task3, task2]
