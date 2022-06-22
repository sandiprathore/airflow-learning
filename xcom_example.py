from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2020, 1, 1)
}
a = "{{dag_run.conf['a']}}"
with DAG('xcom_example_dag', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:
    
    def xcom_push(**kwargs):
        a = kwargs['a']
        print(a)
        kwargs["ti"].xcom_push(key = "a", value = a)

    def xcom_pull(**kwargs):
        pulled_a = kwargs["ti"].xcom_pull(key='a', task_ids=['print_a'])
        print(f'choose best model: {pulled_a}')

    
    x_dag = PythonOperator(
    task_id='print_a',
    python_callable=xcom_push,
    op_kwargs={'a': a}
    )

    x_dag_2 = PythonOperator(
    task_id='print_a_pulled',
    python_callable=xcom_pull,
    )

    x_dag >> x_dag_2