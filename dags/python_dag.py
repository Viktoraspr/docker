from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.database.database_management import DBConnection

default_args = {
    'owner': 'Viktoras',
    'retries': 3,
    'retry_delay': timedelta(minutes=2)
}


def print_value(age, ti):
    name = ti.xcom_pull(task_ids='get_name')
    print(f'Cia yra Python operatorius,{name}, amzius {age}')

    db_conn = DBConnection()
    print(db_conn.get_values_from_job_table())


def get_name():
    return 'Tom'


with DAG(
    dag_id='python_6',
    default_args=default_args,
    description="Lets try to do something",
    start_date=datetime(2023, 10, 12, 0),
    schedule_interval='@daily',
    catchup=False
) as dag:

    task1 = PythonOperator(
        task_id='print_value',
        python_callable=print_value,
        op_kwargs={'age': '20'},
    )

    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name,
    )

    task2 >> task1
