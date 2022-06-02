from datetime import datetime, timedelta
from textwrap import dedent
import os
from airflow.decorators import task

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from rabbitmq_provider.operators.rabbitmq import RabbitMQOperator
from airflow.operators.bash import BashOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.python import BranchPythonOperator
from airflow.operators.python_operator import PythonOperator
from airflow import AirflowException
from airflow.utils.task_group import TaskGroup
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.sensors.filesystem import FileSensor

TIMEOUT = timedelta(days=14)


def task_to_fail():
    raise AirflowException("Please change this step to success to continue")

def download_from_s3(key: str, bucket_name: str, local_path: str) -> str:
    hook = S3Hook('s3_conn')
    file_name = hook.download_file(key=key, bucket_name=bucket_name, local_path=local_path)
    return file_name

def rename_file(**kwargs):
    print(kwargs)
    ti=kwargs['ti']
    print(ti.xcom_pull(task_ids='file_group.download_from_s3'))
    downloaded_file_name = str(ti.xcom_pull(task_ids='file_group.download_from_s3'))
    os.rename(src=downloaded_file_name, dst=f"/fileinput/{kwargs['new_name']}")    

F_NAME = 'airflow-exp-p5-file-list.json'

with DAG(
    '5mid_size_pipeline',

    default_args={
        'depends_on_past': False,
        'email': ['airflow@airflowexperiments.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=15),

    },
    description='mid sized pipeline',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 5, 25),
    catchup=False,
    tags=['extraction pipeline'],
) as dag:
    start_task   = DummyOperator(  task_id= "start"  )
    with TaskGroup("file_group", tooltip="Tasks for files") as file_task_group:
        cleanup = BashOperator(task_id='cleanup_previous',
        bash_command=f'rm -f -- /fileinput/{F_NAME}'
        )
        file_task   = PythonOperator(
        task_id='download_from_s3',
        python_callable=download_from_s3,
        op_kwargs={
            'key': F_NAME,
            'bucket_name': 'git-experiments',
            'local_path': '/fileinput'
        }
        )
        task_rename_file = PythonOperator(
            task_id='rename_file',
            python_callable=rename_file,
            op_kwargs={
                'new_name': F_NAME
            }
        )
        file_sort_task   = DummyOperator(  task_id= "file_sort"  )
        pdf_task   = FileSensor( task_id= "pdf_to_img", 
                poke_interval= 30,  filepath= "/fileinput/p5/*.pdf" )
        img_task   = FileSensor(  task_id= "img_fix"  ,
                poke_interval= 30,  filepath= "/fileinput/p5/*.[jpg|png]" )
        gather_task   = DummyOperator(  task_id= "gather_files"  )
        cleanup >> file_task >> task_rename_file >> file_sort_task >> [pdf_task, img_task] >> gather_task
    classify_task  = DummyOperator(  task_id= "classify"  )
    manual_task_class  = DummyOperator(  task_id= "no_model_classify_manual_label"  )
    perform_img_to_text = DummyOperator(  task_id= "perform_img_to_text"  )
    with TaskGroup("extraction_group", tooltip="Tasks for extractions") as extraction_task_group:
        extract_number_plate = DummyOperator(  task_id= "extract_number_plate"  )
        extract_reciept = DummyOperator(  task_id= "extract_reciept"  )
        extract_checkboxes = DummyOperator(  task_id= "extract_checkboxes"  )
        postprocess = DummyOperator(  task_id= "postprocess"  )
        [extract_number_plate,extract_reciept, extract_checkboxes ] >> postprocess
    rules = DummyOperator(  task_id= "rules"  )
    manual_sign_off = PythonOperator(

        task_id="manual_sign_off",
        python_callable=task_to_fail,
        retries=1,
        retry_delay=TIMEOUT
    )


    stop_task   = DummyOperator(  task_id= "stop"  )



    dag.doc_md = __doc__
    start_task >> file_task_group >> [classify_task, manual_task_class, perform_img_to_text] >> extraction_task_group
    extraction_task_group >> rules >> manual_sign_off >> stop_task