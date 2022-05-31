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


TIMEOUT = timedelta(days=14)


def task_to_fail():
    raise AirflowException("Please change this step to success to continue")

# idea from https://stackoverflow.com/a/59232955
with DAG(
    '4human_non_polling',

    default_args={
        'depends_on_past': False,
        'email': ['airflow@airflowexperiments.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=15),

    },
    description='approval without sensor',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 5, 25),
    catchup=False,
    tags=['non polling intervention'],
) as dag:
    start_task   = DummyOperator(  task_id= "start"  )
    manual_sign_off = PythonOperator(

        task_id="manual_sign_off",
        python_callable=task_to_fail,
        retries=1,
        retry_delay=TIMEOUT
    )


    stop_task   = DummyOperator(  task_id= "stop"  )



    dag.doc_md = __doc__
    start_task >> manual_sign_off >> stop_task