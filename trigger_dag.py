from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.sensors.external_task_sensor import ExternalTaskSensor
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

dag = DAG('hello_external_task_sensor',
          schedule_interval='*/5 * * * *',
          default_args=default_args,
          catchup=False
          )


external_task_sensor = ExternalTaskSensor(
    task_id='external_task_sensor',
    poke_interval=60,
    timeout=180,
    soft_fail=False,
    retries=2,
    external_task_id='task_to_be_sensed',
    external_dag_id='targate_dag',
    dag=dag)


def my_processing_func(**kwargs):
    print("I have sensed the task is complete in a dag")


some_task = PythonOperator(
    task_id='some_task',
    python_callable=my_processing_func,
    dag=dag)

external_task_sensor >> some_task