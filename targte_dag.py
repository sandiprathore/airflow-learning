from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 8, 29, 16, 00),
    'email': ['vipin@cloudwalker.io'],
    'email_on_failure': False,
    'max_active_runs': 1,
    'email_on_retry': False,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('targate_dag',
          schedule_interval='*/5 * * * *',
          default_args=default_args,
          catchup=False
          )


def my_processing_func(**kwargs):
    print("I am task which does something")



task_to_be_sensed = PythonOperator(
    task_id='task_to_be_sensed',
    python_callable=my_processing_func,
    dag=dag)


