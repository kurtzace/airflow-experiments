from datetime import datetime, timedelta
from textwrap import dedent
import os

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from rabbitmq_provider.operators.rabbitmq import RabbitMQOperator
from airflow.operators.bash import BashOperator
from airflow.operators.http_operator import SimpleHttpOperator
os.system("airflow connections add --conn-type 'http' --conn-host 'https://gorest.co.in/public/v2' api_posts")
os.system("airflow connections add  --conn-uri 'amqp://guest:guest@rabbitmq:5672/' 'rabbitmq_connid'")



with DAG(
    '1airflow_expriments',
    
    default_args={
        'depends_on_past': False,
        'email': ['airflow@airflowexperiments.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
        
    },
    description='A simple DAG',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2022, 5, 25),
    catchup=False,
    tags=['airflow-experiments'],
) as dag:
    t1 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    http_operator = SimpleHttpOperator(
        task_id='http_task', 
        http_conn_id='api_posts',
        endpoint='posts/',
        method='GET',
        log_response=True
        )
    rabbit_operator = RabbitMQOperator(
        task_id='rabbit_task',
        rabbitmq_conn_id='rabbitmq_connid',
        exchange='',
        routing_key='test',
        message='http_response_recieved'
    )
        
    t1.doc_md = dedent(
        """\
    #### Task Documentation
    
    """
    )

    dag.doc_md = __doc__ 
    t1 >> http_operator
    http_operator >> rabbit_operator