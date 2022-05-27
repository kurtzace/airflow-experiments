from datetime import datetime, timedelta
import os
import json
import time
from airflow.sensors.filesystem import FileSensor
from airflow.operators.dummy_operator import DummyOperator
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.python_operator import PythonOperator

os.system("airflow connections add --conn-type 'fs' fs_default")
default_args={
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
        
    }
def create_dag(schedule, default_args, definition):
    """Create dags dynamically."""
    with DAG(
        definition["name"], schedule_interval=schedule, default_args=default_args,
        start_date=datetime(2022, 5, 25),
        catchup=False,
        tags=['dynamically'],
    ) as dag:

        tasks = {}
        for node in definition["nodes"]:
            operator = load_operator(node["_type"])
            params = node["parameters"]

            node_name = node["name"].replace(" ", "")
            params["task_id"] = node_name
            params["dag"] = dag
            tasks[node_name] = operator(**params)

        for node_name, downstream_conn in definition["connections"].items():
            for ds_task in downstream_conn:
                tasks[node_name] >> tasks[ds_task]

    globals()[definition["name"]] = dag
    return dag

def load_operator(name):
    """Load operators dynamically"""
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod



def create_dag_from_json():
    dag_file= '/fileinput/input_dag.json'
    if(os.path.exists(dag_file)):
        dag_payload = json.load(open(dag_file, encoding = 'utf-8'))
        return create_dag(None, default_args, dag_payload)


# with DAG(
#     '2create_dag_json',
    
#     default_args=default_args,
#     description='Creare Dag from JSON in docker/airflow/fileinput',
#     schedule_interval=timedelta(days=1),
#     start_date=datetime(2022, 5, 25),
#     catchup=False,
#     tags=['airflow-experiments'],
# ) as dag:
#     start_task  = DummyOperator(  task_id= "start" )
#     stop_task   = DummyOperator(  task_id= "stop"  )
#     sensor_task = FileSensor( task_id= "json_sensor_task", recursive=False,  
#     filepath= "/fileinput",
#     poke_interval=30 )
#     json_task = PythonOperator(task_id='json_task', 
#     python_callable=create_dag_from_json)


#start_task >> sensor_task >> json_task >> stop_task
create_dag_from_json()