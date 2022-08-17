<font size="2">

![apache_Airflow](https://user-images.githubusercontent.com/93520937/175787333-5089e753-5d09-4396-8f71-33514a48f199.png)



##### What is Airflow?
Apache Airflow is an open-source workflow management platform. It began in October 2014 at Airbnb as a solution for managing the company's increasingly complex workflows. Airbnb's creation of Airflow enabled them to programmatically author, schedule, and monitor their workflows via the built-in Airflow user interface. Airflow is a data transformation pipeline ETL (Extract, Transform, Load) workflow orchestration tool.


##### Workflow is designed in Airflow

* A directed acyclic graph (DAG) is used to design an Airflow workflow. That is to say, when creating a workflow, consider how it can be divided into tasks that can be completed independently. The tasks can then be combined into a graph to form a logical whole.
* The overall logic of your workflow is based on the shape of the graph. An Airflow DAG can have multiple branches, and you can choose which ones to follow and which to skip during workflow execution.
* Airflow could be completely stopped, and able to run workflows would then resume through restarting the last unfinished task.
* It is important to remember that airflow operators can be run more than once when designing airflow operators. Each task should be idempotent, or capable of being performed multiple times without causing unintended consequences.

##### Airflow Architecture and its components
There are four major components to airflow.

1. Webserver
2. Scheduler
3. Executor
4. Worker


   1. **Webserver**
   This is the Airflow UI built on the Flask, which provides an overview of the overall health of various DAGs and helps visualise various components and states of every DAG. For the Airflow setup, the Web Server also allows you to manage users, roles, and different configurations.
   
   2. **Scheduler**
   Every n seconds, the scheduler walks over the DAGs and schedules the task to be executed.

   3. **Executor** 
   Executor is another internal component of the scheduler.
   The executors are the components that actually execute the tasks, while the Scheduler orchestrates them. Airflow has different types of executors, including SequentialExecutor, LocalExecutor, CeleryExecutor and KubernetesExecutor. People generally choose the executor which is best for their use case.

   4. **Worker**
    Workers are responsible to run the task that the executor has given them.

<p align="center">
 <img  src="https://user-images.githubusercontent.com/93520937/183026129-2ee5006a-00d7-43b8-b813-1471ecac92e8.png" alt="Material Bread logo"><br>
 <b>airflow architecture</b>
</p>

##### Executors in Airflow
The executors are the components that actually execute the tasks, while the Scheduler orchestrates them. Airflow has different types of executors, including SequentialExecutor, LocalExecutor, CeleryExecutor and KubernetesExecutor. People generally choose the executor which is best for their use case.

1. **SequentialExecutor**
Only one task is executed at a time by SequentialExecutor. The scheduler and the workers both use the same machine.
2. **LocalExecutor**
LocalExecutor is the same as the Sequential Executor, except it can run multiple tasks at a time.
3. **CeleryExecutor**
Celery is a Python framework for running distributed asynchronous tasks.
As a result, CeleryExecutor has long been a part of Airflow, even before Kubernetes.
CeleryExecutors has a fixed number of workers on standby to take on tasks when they become available.
4. **KubernetesExecutor**
Each task is run by KubernetesExecutor in its own Kubernetes pod. It, unlike Celery, spins up worker pods on demand, allowing for the most efficient use of resources

##### Install airflow on ubuntu 18.0

* Note : You need to use pip to install apache airflow on Linux operating systems.
 install Airflow Dependencies


##### For airflow to work properly you need to install all its dependencies.
```bash
sudo apt-get install libmysqlclient-dev
sudo apt-get install libssl-dev
sudo apt-get install libkrb5-dev
```

**create virtual environment**
```bash
sudo apt install python3-virtualenv
virtualenv airflow_env
source airflow_env/bin/activate
```

**Installing Apache Airflow**
```bash
export AIRFLOW_HOME=~/airflow
pip3 install apache-airflow
pip3 install typing_extensions
```

**initialize the database**
```bash
airflow db init
```

```bash
* Go to home/airflow directory
* Open airflow.cfg
    *   repalce "load_examples = True" to "load_examples = False"
    *   save the file 
```

create a dags folder 
```bash
mkdir dags
``` 

**Create user**
```bash
airflow users create --username admin --password admin --firstname admin --lastname admin --role Admin --email admin@gmail.com
```

**Reset and initialize airflow database** 
```bash
airflow db reset -y && airflow db init
```

**start the web server, default port is 8080**
```bash
airflow webserver 
```

**Run airflow webserver with nohup**
```bash
nohup airflow webserver > airflow_webserver.log &
```

**Start the scheduler.** 
```bash
airflow scheduler
```

**Run airflow scheduler with nohup**
```bash
nohup airflow scheduler > airflow_scheduler.log &
```

**To uninstall apache-airflow:**
```bash
pip uninstall apache-airflow
```

##### The Basics of airflow 

##### Define your DAG: the right way
In Airflow, a DAG is a collection of all the tasks you want to run, organized in a way that reflects their relationships and dependencies.
 
**Step 1: make the imports**
The first step is to import the classes you need. 
To create a DAG in Airflow, you always have to import the DAG class.
 
**Step 2: Create the Airflow DAG object**
A DAG object has two important parameters : start_Date and schedule_Interval
start_date →date at which your DAG starts being scheduled.
schedule_interval → interval of time at which your DAG gets triggered. Every 10 mins, every day, every month and so on.
 
**For Example :**
start_date → 1 january 2021, 10:00:00 AM (midnight)
schedule _interval → 10 minutes 
Your task will be effectively triggered on 1 january 2021, at 10:10:00 AM ,then 10:20:00 AM, then 10:30:00 AM and in every 10 mins.


```py
with DAG('dag',
 default_args=default_args,
 schedule_interval='*/10 * * * *',
 catchup=False):
# TIMEDELTA OBJECT
with DAG('dag',
 default_args=default_args,
 schedule_interval=timedelta(minutes=10),
 catchup=False):
 ```


##### A DAG object parameters:

```
dag_id → unique identifier of the DAG across all DAGs.
dagrun_timeout → it sets the execution timeout of a DAG Run.
Tags → filter a dag by tag name. you can add tags in each dag.
catchup → Airflow automatically runs non triggered DAG Runs between the latest executed DAG Run and the current date. For best practice always set catchup as False.
Backfill →If for some reason we want to re-run DAGs on certain schedules manually we can use the following CLI command to do so.
airflow backfill -m -s <START_DATE> -e <END_DATE> <DAG_NAME>
 ```
#### Airflow operators

* #####  PythonOperator

```py
from airflow import DAG
from airflow.operators.python import PythonOperator
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

* #####  BashOperator
```py
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

#### Master your Variables

**Variables** in Airflow are nothing more than objects with keys. Any value that will be stored in metadatabase and so instead of hardcoding the same value all over the tasks you just need to fetch the same variable modified that is divided by well and the modification will be applied automatically everywhere which is much better and this gives you lots of flexibility.

##### Add variable in airflow 
Go to admin --> variable

![image](https://user-images.githubusercontent.com/93520937/175788856-15920084-700e-4fb9-88b9-e85baa6b560b.png)


* click on "+"  icon to add new variable
![image](https://user-images.githubusercontent.com/93520937/175788904-47026fcf-8e24-43bf-a75e-2ac2da700cec.png)


* Add key and value of variable and click on save button
![image](https://user-images.githubusercontent.com/93520937/175788991-03e2bcc4-5d50-486d-b81e-a3eb3c7e385e.png)


To add variable firstly you have to import package:
```py
from airflow.models import Variable
```

###### Example: dag
```py
from airflow  import dag
from airflow.operators.python import PythonOperator
from datetime import datetime , timedelta

def  get_variable():
    from airflow.models import Variables
	Partner = Variable.get("my_dag_parameter")
	print(Partner)

With DAG (
    dag_id = "my_dag", 
    description='DAG in charge of process,
    start_date=datetime(2021, 1 ,1), schedulw_interval=@daily,
	dagrun_timeout= timedelta(minutes=10), tags="data_scince",
	catchup=False, max_active_runs=1
) as dag:
        extract = PyhtonOperator(
        task_id="extract",
        python_callable=get_variable
        )
 ```


What if you have a variable that starts an API or secret key you definitely don't want to have your key exposed. So you can create a variable of your secret keys, airflow automatically hide the value of the variable and secure your credentials.

What if you have a multiple variable? You have to create multiple connections or variables for each other, but it is not a good practice.
You can set multiple values of variables on a single key in json format and it will make your dag cleaner. Also it's a good practice to define veriables.

**Let's take an example**
```py
"AWS_ACCESS_KEY_ID": "<>" 
"AWS_SECRET_ACCESS_KEY": "<>"
"AWS_DEFAULT_REGION": "<>"
 ```

As we know how to set variables in Airflow UI, but this time we have to define our variable values in json format.
```json
{"AWS_ACCESS_KEY_ID": "<>", "AWS_SECRET_ACCESS_KEY": "<>", "AWS_DEFAULT_REGION": "<>"}
```

##### Method 1 to fetch variable:
```py
from airflow  import dag
from airflow.operators.python import PythonOperator
from datetime import datetime , timedelta

def extract_variable_from_airflow(variable_name:str)-> dict:"""
    Get the veriavles from airflow 
    
    Parameters
    ----------
    variable_name: variable name that we want to get from airflow
    
    Returns
    -------
    airflow_variable : variable value from airflow
    """
    from airflow.models import Variables

    airflow_variable = Variable.get(variable_name, deserialize_json=True)
    return airflow_variable

def get_veriable():
    # here we want to extract aws_authorization variable 
    aws_authorization = extract_variable_from_airflow(aws_authorization)
    AWS_ACCESS_KEY_ID = aws_authorization['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = aws_authorization['AWS_SECRET_ACCESS_KEY']
    AWS_DEFAULT_REGION = aws_authorizatio['AWS_DEFAULT_REGION']



With DAG (
    dag_id = "my_dag",
    description = 'DAG to get Variables,
    start_date = datetime(2021, 1 ,1), 
    schedulw_interval = @daily,
    dagrun_timeout = timedelta(minutes=10), 
    tags = "data_scince",
    catchup = False, 
    max_active_runs = 1
) as dag:
    extract = PyhtonOperator(
    task_id = "extract_var",
    python_callable=get_veriable
    )
 ```

Also we can fetch variables using jinja template
```py
extract = PyhtonOperator(
task_id="extract",
python_callable=_extract
op_args=["{{var.json.my_dag_partner.name}}"]
)
 ```

###### Sharing data with XCOMs and limitations  

Xcom is a mechanism in airflow allowing you to share it between your tasks. Basically you want to share a value like a string or some data you can put into an XCOM and this XCOM is an object that will be stored within your meter database with the key and the value that you want to store. Then you will be able to pull that XCOM from another task so that you can share data between your tasks. It is as simple as that but there are some limitations and you have to be aware of them and you will end up with some troubles. Let's begin with the limitations and then the different ways of getting your xcom and the last way is my favorite one. Let's get started in your data pipeline.

</font>

* ##### Read variable with BashOperator
```py
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

* ##### Pass and Read parameters to BashOperator

```py
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


##### We can also pass parameters at dag run 
* click on button to run dag and select "Trigger DAG W/config"

 ![image](https://user-images.githubusercontent.com/93520937/175790067-6307a5cc-3117-4b5d-8bf9-cb696c39c862.png) 

* pass your parameters in json formate 

 ![image](https://user-images.githubusercontent.com/93520937/175790172-9c1b2405-191d-4b51-88cc-c942df993089.png)

* Read runtime parameters to BashOperator
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