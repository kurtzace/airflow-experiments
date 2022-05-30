from datetime import datetime, timedelta
from textwrap import dedent
import os
from airflow.decorators import task
from pymongo import MongoClient
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from rabbitmq_provider.operators.rabbitmq import RabbitMQOperator
from airflow.operators.bash import BashOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.python import BranchPythonOperator

myip = '192.168.0.127'

os.system(f"airflow connections add  --conn-type http --conn-host 'http://{myip}:60001' rest_local_ip1")


@task(task_id="mongo_task")
def restcall(**kwargs):
    ti=kwargs['ti']
    import urllib.request
    webUrl  = urllib.request.urlopen(f'http://{myip}:60001/save/'+ti.xcom_pull(task_ids='push_jobid'))
    print("result code:"+ str(webUrl.getcode()))
    return ti.xcom_pull(task_ids='push_jobid')

def choose_best_model(**kwargs):
    ti=kwargs['ti']
    print(ti.xcom_pull(task_ids='http_task'))
    input=ti.xcom_pull(task_ids='http_task')
    if(input=='true'):
        return "accurate"
    else:
        return "inaccurate"


with DAG(
    '3human_in_loop',

    default_args={
        'depends_on_past': False,
        'email': ['airflow@airflowexperiments.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),

    },
    description='Human in loop',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 5, 25),
    catchup=False,
    tags=['apiToResume'],
) as dag:
    t1 = BashOperator(
        task_id='push_jobid',
        bash_command='jobid=$(date +"%y-%m%d-%H%M") && '
        'echo $jobid'
    )
    
    task_pending_check = HttpSensor(
        task_id='pending_check',
        http_conn_id='rest_local_ip1',
        endpoint='/gethumanstatus/{{task_instance.xcom_pull(task_ids=\'mongo_task\')}}',
        request_params={},
        response_check=lambda response: "pending" not in response.text,
        poke_interval=10,
    )
    http_operator = SimpleHttpOperator(
            task_id='http_task', 
            http_conn_id='rest_local_ip1',
            endpoint='/gethumanstatus/{{task_instance.xcom_pull(task_ids=\'mongo_task\')}}',
            method='GET'
            )
    # task_approval = BashOperator(
    #     task_id='approval_flow',
    #     bash_command='echo "Approval Flow" && '
    #     f'echo {http_operator.output}'
    # )
    choose_best_model = BranchPythonOperator(
    task_id='choose_best_model',
    python_callable=choose_best_model
    )
    accurate = DummyOperator(
    task_id='accurate'
    )
    inaccurate = DummyOperator(
    task_id='inaccurate'
    )
    


    stop_task   = DummyOperator(  task_id= "stop"  )



    dag.doc_md = __doc__
    t1 >> restcall() >> task_pending_check >> http_operator >> choose_best_model >> [accurate, inaccurate] >> stop_task