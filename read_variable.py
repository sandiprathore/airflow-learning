from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

with DAG(dag_id='bash_dag', schedule_interval=None, start_date=datetime(2020, 1, 1), catchup=False) as dag:
    bash_task = BashOperator(task_id='bash_task', bash_command="echo name is {{var.value.name}}")