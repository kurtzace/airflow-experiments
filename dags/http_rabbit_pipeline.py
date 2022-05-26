from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.http_operator import SimpleHttpOperator
#from airflow.operators import MongoOperator
import json
import os
from pymongo import MongoClient


os.system("airflow connections --add --conn_id 'api_posts' --conn_type HTTP --conn_host 'https://gorest.co.in/public/v2'")

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
    


dag = DAG('http_rabbit', description='http Rabbit DAG',
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


#TODO understand mongo operator
# mongo_operator = MongoOperator(task_id='mongo_task', 
#     mongo_conn_id='my_mongo',
#     mongo_collection='posts_collection',
#     mongo_database='blog',
#     mongo_query=None,
#      dag=dag)

http_operator >> mongo_operator