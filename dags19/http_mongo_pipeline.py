from datetime import datetime
from email import message
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.http_operator import SimpleHttpOperator
#from airflow.operators import MongoOperator
import json
import os
from pymongo import MongoClient
from airflow.contrib.sensors.file_sensor import FileSensor
# from rabbitmq_provider.operators.rabbitmq import RabbitMQOperator


os.system("airflow connections --add --conn_id 'api_posts' --conn_type HTTP --conn_host 'https://gorest.co.in/public/v2'")
#os.system("airflow connections --add --conn_id 'rabbitmq_conn' --conn_host 'amqp://guest:guest@localhost:5672'")


def mongocall(**kwargs):
    ti=kwargs['ti']
    print("Entering Mongo Block")
    http_value = ti.xcom_pull(task_ids='http_task')
    print(http_value)
    client=MongoClient("mongodb://mongo:27017/")
    db=client['test']
    coll=db['postcollection']
    coll.insert_many(json.loads(http_value))
    return True
    




dag = DAG('http_mongo', description='http mongo DAG',
          schedule_interval='@daily',
          start_date=datetime(2022, 5, 20), catchup=False)

http_operator = SimpleHttpOperator(task_id='http_task', 
    http_conn_id='api_posts',
    endpoint='posts/',
    method='GET',
    response_filter = lambda resp: json.loads(resp.text),
    log_response=True,
    xcom_push=True, #send data to next node
     dag=dag)

mongo_operator = PythonOperator(task_id='mongo_task',
    python_callable=mongocall, dag=dag,
    provide_context=True)


dummy_operator = DummyOperator(task_id='dummy_task', dag=dag)

file_task = FileSensor( task_id= "file_sensor_task", 
    poke_interval= 30,  filepath= "/fileinput" )

##TODO rabbitmq runs into error as on readme
# rabbit_operator = RabbitMQOperator(
#     task_id='rabbit_task',
#     rabbitmq_conn_id='rabbitmq_conn',
#     exchange='',
#     routing_key='test',
#     message='http_response_recieved'
# )

#TODO understand mongo operator
# mongo_operator = MongoOperator(task_id='mongo_task', 
#     mongo_conn_id='my_mongo',
#     mongo_collection='posts_collection',
#     mongo_database='blog',
#     mongo_query=None,
#      dag=dag)

file_task >> http_operator
http_operator >> [mongo_operator, dummy_operator]