## Guides
- [Productionalizing Data Pipelines with Apache Airflow by Axel Sirota | Pluralsight](https://www.pluralsight.com/courses/productionalizing-data-pipelines-apache-airflow)
- [git study](https://github.com/mikeroyal/Apache-Airflow-Guide)
- [express youtube guide](https://www.youtube.com/watch?v=2v9AKewyUEo), [whose git is](https://github.com/soumilshah1995/Learn-Apache-Airflow-in-easy-way-/tree/main/project)

## Getting started project
[git productionalizing-data-pipelines-airflow](https://github.com/axel-sirota/productionalizing-data-pipelines-airflow)

## instructions to run the project
```
sudo docker-compose build
sudo docker-compose up
```

## providers
- [rabbit](https://github.com/tes/airflow-provider-rabbitmq)
- http  - pip install 'apache-airflow-providers-http', [sample dag](https://github.com/apache/airflow/blob/main/airflow/providers/http/example_dags/example_http.py), [blog](https://betterdatascience.com/apache-airflow-rest-api/), [example rest apis that we could call](https://gorest.co.in/)
- mongo - pip install 'apache-airflow-providers-mongo' - [connection troubleshooting](https://stackoverflow.com/questions/64865387/setting-mongodb-connection-with-airflow), [sample dag](https://github.com/axel-sirota/productionalizing-data-pipelines-airflow/blob/main/module5-demo3/dags/mongo_dag.py)

## How to 
- [first dag](https://progressivecoder.com/airflow-dag-example-create-your-first-dag/)
- [parallel dag](https://github.com/axel-sirota/productionalizing-data-pipelines-airflow/blob/main/module6-demo2/dags/parallel_dag.py)
- files detector [link1](https://big-data-demystified.ninja/2019/11/14/airflow-file-sensor-example-airflow-demystified/), [troubleshooting](https://stackoverflow.com/questions/54791596/any-example-of-airflow-filesensor)
- [branch](https://github.com/axel-sirota/productionalizing-data-pipelines-airflow/blob/main/module5-demo2/dags/invoices_dag.py)
- Stopping a dag: You can set the running tasks to failed with [Set a state of task instances](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_set_task_instances_state)  , Alternately If you want the DAG to not schedule any more tasks you can set it to Pause with [Update a DAG](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/patch_dag)
- [trigger via API blog](https://brocktibert.com/post/trigger-airflow-dags-via-the-rest-api/), [start api blog](https://hevodata.com/learn/airflow-rest-api/)
- [create dag via UI discussion](https://stackoverflow.com/questions/48986732/airflow-creating-a-dag-in-airflow-via-ui), using [cwl we can describe workflow in yml syntax](https://cwl-airflow.readthedocs.io/en/latest/readme/quick_start.html)
- Convert json to Apache Dag: [one blog by geek culture](https://medium.com/geekculture/how-to-dynamically-create-apache-airflow-dag-s-via-only-json-rationalize-tech-47f227071c78)
- [share data between tasks in Airflow](https://marclamberti.com/blog/airflow-dag-creating-your-first-dag-in-5-minutes/), [eg from airflow docs](https://github.com/apache/airflow/blob/main/airflow/example_dags/example_xcom.py), [Push and Pull same ID from several operator](https://big-data-demystified.ninja/2020/04/15/airflow-xcoms-example-airflow-demystified/)
