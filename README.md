# airflow
##### Install airflow on ubuntu 18.0

* Note : You need to use pip to install apache airflow on Linux operating systems.
 install Airflow Dependencies

For airflow to work properly you need to install all its dependencies.

```
sudo apt-get install libmysqlclient-dev
sudo apt-get install libssl-dev
sudo apt-get install libkrb5-dev
```


create virtual environment
```
sudo apt install python3-virtualenv
virtualenv airflow_env
source airflow_env/bin/activate
```

Installing Apache Airflow
```
export AIRFLOW_HOME=~/airflow
pip3 install apache-airflow
pip3 install typing_extensions
```
###### initialize the database
```
airflow db inita
```

Create user
```
airflow users create --username admin --password admin --firstname admin --lastname admin --role Admin --email admin@gmail.com
```
Reset airflow database 
```
airflow db reset -y && airflow db init
```

start the web server, default port is 8080
```
airflow webserver 
```

Run airflow with nohup
```
nohup airflow webserver > myoutput.log &
```

start the scheduler. 
```
airflow scheduler
```

To uninstall apache-airflow:
```
pip uninstall apache-airflow
```
