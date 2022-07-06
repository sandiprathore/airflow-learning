from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator

def process_runtime_parameters_func(**context: dict):
    """
    if runtime parameters passed overwrite the default parameters  
    param: runtime conf 
    """
    ti = context['ti']
    DAG_PARAMETERS = {
        "S3_BUCKET": "labs-airflow-data",
        "INPUT_PATH": "ocred_pdfs/dev-1-v-2-2-2/input_pdfs/", 
        "OUTPUT_PATH": "ocred_pdfs/dev-1-v-2-2-2/output_pdfs/",
        "PROJECT_NAME": ""
     }
    runtime_conf = context['dag_run'].conf
    if runtime_conf:
        if "PROJECT_NAME" in  runtime_conf.keys():
            if runtime_conf["PROJECT_NAME"]:
                for key in runtime_conf.keys():
                    if key in DAG_PARAMETERS.keys():
                        DAG_PARAMETERS[key] = runtime_conf[key]
                ti.xcom_push(key = "DAG_PARAMETERS", value = DAG_PARAMETERS) 
                return 'process_scanned_pdf_files' 
    print('INFO: Function: "process_runtime_parameters_func": PROJECT_NAME not found in runtime parameters')
    return 'no_project_path'


def aws_auth_init(aws_authorization):
    """
    aws authorization
    param: aws_authorization variable 
    """
    import os
    os.environ["AWS_ACCESS_KEY_ID"] = aws_authorization["AWS_ACCESS_KEY_ID"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = aws_authorization["AWS_SECRET_ACCESS_KEY"]
    os.environ["AWS_DEFAULT_REGION"] = aws_authorization["AWS_DEFAULT_REGION"]


def process_scanned_pdf_func(**context):
    """
    process scanned pdf to searchable pdf 
    param: DAG PARAMETERS 
    """
    import boto3
    import os 
    from airflow.models import Variable

    ## pulling parameters from "process_run_time_parameters" task 
    ti = context['ti']
    runtime_parameters = ti.xcom_pull(key='DAG_PARAMETERS', task_ids='process_run_time_parameters')

    # parameters
    s3_bucket = runtime_parameters['S3_BUCKET']
    input_path = runtime_parameters['INPUT_PATH']
    project_path = runtime_parameters['PROJECT_NAME']
    output_Prefix = runtime_parameters['OUTPUT_PATH']
    
    # aws_authorization
    aws_authorization = Variable.get('aws_authorization', deserialize_json=True)
    aws_auth_init(aws_authorization)

    # list of pdf file to process 
    Prefix = f'{input_path}{project_path}'
    s3 = boto3.resource('s3')
    # s3_client = boto3.client('s3')

    my_bucket = s3.Bucket(s3_bucket)
    list_of_files = []
    for file in my_bucket.objects.filter(Prefix=Prefix):
        file_name=file.key
        if file_name.lower().find(".pdf")!=-1:
                list_of_files.append(file.key)

    if not list_of_files:
        # if pdf files not found in project
        print(f'INFO: Function: "process_scanned_pdf_func":  No pdf files found in "{project_path}" project')
        return 'no_pdf_file_found'

    # if pdf files available in project
    # how many pdf files available 
    print(f'INFO: Function: "process_scanned_pdf_func": {len(list_of_files)} pdf files found in "{project_path}" project')
    for file in list_of_files:
        print(f'INFO: Function: "process_scanned_pdf_func": Currently processing "{file}"')
        
        # download the file
        file_name = os.path.basename(file)
        my_bucket.download_file(file, file_name)
       
        # upload the file 
        output_file = file.replace(input_path,'')
        output_path = f'{output_Prefix}{output_file}'
        my_bucket.upload_file(file_name, output_path)

        # remove file from local 
        os.remove(file_name)
        print(f'INFO: Function: "process_scanned_pdf_func": "{file_name}" processed successfully')
    return 'end'

with DAG(
    dag_id='scanned_to_searchable_pdf', 
    schedule_interval=None, 
    start_date=datetime(2019, 1, 10), 
    catchup=False
)as dag:
        # task: To process runtime parameters
        process_runtime_parameters = BranchPythonOperator(
                task_id='process_run_time_parameters',
                python_callable=process_runtime_parameters_func,
                provide_context=True,
                do_xcom_push=False
                )

        # task: If PROJECT_NAME not available in runtime parameter
        no_project_path =  DummyOperator(
                task_id='no_project_path'
                )

        # task: To process scanned pdf files 
        process_scanned_pdf_file =  BranchPythonOperator(
                task_id='process_scanned_pdf_files',
                python_callable=process_scanned_pdf_func,
                provide_context=True
                )

        # task: if pdf files not found   
        no_pdf_file_found =  DummyOperator(
            task_id='no_pdf_file_found'
            )

        # task: End of the dag
        end = DummyOperator(
            task_id='end',
            trigger_rule='one_success'
            )

process_runtime_parameters >> [ process_scanned_pdf_file, no_project_path] >> end
process_scanned_pdf_file >> no_pdf_file_found >> end