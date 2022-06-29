
![apache_Airflow](https://user-images.githubusercontent.com/93520937/175787333-5089e753-5d09-4396-8f71-33514a48f199.png)


##### Install airflow on ubuntu 18.0

* Note : You need to use pip to install apache airflow on Linux operating systems.
 install Airflow Dependencies

###### For airflow to work properly you need to install all its dependencies.

```
sudo apt-get install libmysqlclient-dev
sudo apt-get install libssl-dev
sudo apt-get install libkrb5-dev
```


###### create virtual environment
```
sudo apt install python3-virtualenv
virtualenv airflow_env
source airflow_env/bin/activate
```

###### Installing Apache Airflow
```
export AIRFLOW_HOME=~/airflow
pip3 install apache-airflow
pip3 install typing_extensions
```
###### initialize the database
```
airflow db init
```
* ###### Go to home/airflow directory
* ###### Open airflow.cfg
    *  ###### repalce "load_examples = True" to "load_examples = False"
    *  ###### save the file 

create a dags folder 
```
mkdir dags
``` 

###### Create user
```
airflow users create --username admin --password admin --firstname admin --lastname admin --role Admin --email admin@gmail.com
```
###### Reset and initialize airflow database 
```
airflow db reset -y && airflow db init
```

###### start the web server, default port is 8080
```
airflow webserver 
```

###### Run airflow webserver with nohup
```
nohup airflow webserver > myoutput.log &
```

###### start the scheduler. 
```
airflow scheduler
```

###### Run airflow scheduler with nohup
```
nohup airflow scheduler > myoutput.log &
```

###### To uninstall apache-airflow:
```
pip uninstall apache-airflow
```


#### airflow operators

* ######  PythonOperator

```
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def ex_func():
    print('Hello! welcome to airflow')

with DAG('python_example', 
    schedule_interval=None, 
    start_date=datetime(2018, 11, 1), 
    catchup=False) as dag:
        python_task	= PythonOperator(task_id='python_task', python_callable=ex_func)

python_task
      
```
* ######  BashOperator
```
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

with DAG(dag_id='bash_example', 
    schedule_interval=None, 
    start_date=datetime(2020, 1, 1), 
    catchup=False) as dag:
        bash_task = BashOperator(task_id='bash_task', 
            bash_command="echo 'Hello! welcome to airflow'")

bash_task
```

##### Add variable in airflow 
* ###### Go to admin --> variable 

![image](https://user-images.githubusercontent.com/93520937/175788856-15920084-700e-4fb9-88b9-e85baa6b560b.png)

* ###### click on "+"  icon to add new variable

![image](https://user-images.githubusercontent.com/93520937/175788904-47026fcf-8e24-43bf-a75e-2ac2da700cec.png)

* ###### Add key and value of variable and click on save button

![image](https://user-images.githubusercontent.com/93520937/175788991-03e2bcc4-5d50-486d-b81e-a3eb3c7e385e.png)

* ######  Read variable with BashOperator
```

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

with DAG(dag_id='read_ver_with_bash', 
    schedule_interval=None, 
    start_date=datetime(2020, 1, 1), 
    catchup=False) as dag:
        read_ver_with_bash = BashOperator(task_id='read_variable', 
                    bash_command="echo Welcome {{var.value.name}}"
                    )

read_ver_with_bash
```

* ###### Pass and Read parameters to BashOperator

```
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

with DAG(dag_id='read_para_with_bash', 
    schedule_interval=None, 
    start_date=datetime(2020, 1, 1), 
    catchup=False) as dag:
        read_para = BashOperator(
        task_id='read_para',
        bash_command="echo The para is {{params.KEY}}",
        params = {'KEY' : 'value'}
    )

read_para
```

###### We can also pass parameters at dag run 
* ###### click on button to run dag and select "Trigger DAG W/config"

 ![image](https://user-images.githubusercontent.com/93520937/175790067-6307a5cc-3117-4b5d-8bf9-cb696c39c862.png) 

* ###### pass your parameters in json formate 

 ![image](https://user-images.githubusercontent.com/93520937/175790172-9c1b2405-191d-4b51-88cc-c942df993089.png)

* ###### Read runtime parameters to BashOperator
```
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

with DAG(dag_id='read_runtime_para_with_bash', 
    schedule_interval=None, 
    start_date=datetime(2020, 1, 1), 
    catchup=False) as dag:
        read_runtime_para = BashOperator(
        task_id='read_runtime_para',
        bash_command="echo The para is {{dag_run.conf['name']}}" 
    )

read_runtime_para
```