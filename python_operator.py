from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# pyhton function 
def my_func():
    print('Hello from my_func')

with DAG('python_dag', description='Python DAG', schedule_interval='*/5 * * * *', start_date=datetime(2018, 11, 1), catchup=False) as dag:
        #calling to function  
        python_task	= PythonOperator(task_id='python_task', python_callable=my_func)