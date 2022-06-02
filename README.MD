# Airflow 2.0
## Guide
- [setup](https://www.youtube.com/watch?v=aTaytcxy2Ck) and [official doc](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html)
- [diff b/w 1.x and 2.0](https://www.youtube.com/watch?v=mzu4eYOy-Ak)
- [foundation dockercompose](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbWdRaG0xNFRyWDNmc0RkSG1jXzk0eTNkR0dFUXxBQ3Jtc0tuRUl1NHdXQ1hjVTFvLVJaWEFRcUZaM3RQSEN4anpodnNzYnJfblV6STdQZlhPQmhuVEVOcTMxb2FaWnBEY2tPNy1MRWFOd3Nnc1RnSlFlMXZ4WkR0YUtESXQzY1JFOXF2emlybjkwYXY3cWs1UXhqTQ&q=https%3A%2F%2Fairflow.apache.org%2Fdocs%2Fapache-airflow%2Fstable%2Fdocker-compose.yaml&v=aTaytcxy2Ck)

## instructions to run
### first time 
- ensure Install Docker Compose v1.29.1 and newer on your workstation.

in ubuntu
```
sudo apt-get update
sudo apt-get install docker-compose-plugin
```
- echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
- sudo docker compose up airflow-init
### every time
- sudo docker compose up
- signin page - type airflow and airflow
- view dags 2.0 view
![image](https://user-images.githubusercontent.com/2136211/170602797-0f85ec51-a5cf-42eb-a0c0-dd2d59b79987.png)

- run 1airflow_experiments
whose graph is 
![image](https://user-images.githubusercontent.com/2136211/170651732-903d020b-234d-4a54-a72d-db702fce9664.png)

see rabbitmq message
![image](https://user-images.githubusercontent.com/2136211/170651573-40e0ed46-628d-42a3-b6bd-6a4d8a304fa4.png)


### 2nd dag is dynamically generated from json
docker/airflow/fileinput/input_dag.json

### 3rd one is human_in_loop

![image](https://user-images.githubusercontent.com/2136211/171000787-d04f787a-0583-4e8d-ae15-a9db63d974a5.png)

replace myip with your ip in 3human....py by running
```
#in ubuntu
hostname -I
```

ensure you run both docker composes
```
#using docker-compose version 1.27.4,
sudo docker-compose -f docker-compose19.yml build
sudo docker-compose -f docker-compose19.yml  up
sudo docker compose  up
```

....19.yml starts API and mongo
normal ynl starts airflow and rabbit

after it is triggered.

you will see that pending runs infinitely 

it is waiting for human

so copy the jobid from xcom tab of mongo_task

![image](https://user-images.githubusercontent.com/2136211/171001487-221dfd63-130d-483d-9217-8f6d3b6d92df.png)

then call api by either visiting http://localhost:60001/docs

or

call
```
curl -X 'GET' \
  'http://localhost:60001/sethumaninput/22-0530-1314?status=false' \
  -H 'accept: application/json'
```

depending on which (status) accurate or inaccurate flow is called



### Rest call attempt 
```
ENDPOINT_URL="http://localhost:8080/"
curl -X GET  \
    --user "airflow:airflow" \
    "${ENDPOINT_URL}/api/v1/pools"
```

### 4th human non polling 
Run the 4th dag

visit graph and get details as highlighted

![image](https://user-images.githubusercontent.com/2136211/171181806-975dbc70-1d48-43f3-8e38-91f05bdc32c9.png)


call the following endpoint and mark as success (i.e emulated human action)

```
ENDPOINT_URL="http://localhost:8080/"
curl -X POST  \
    --user "airflow:airflow" \
    -H 'Content-Type: application/json' \
    "${ENDPOINT_URL}api/v1/dags/4human_non_polling/updateTaskInstancesState" \
    -d "{ \"dry_run\": false, \"task_id\": \"manual_sign_off\", \
    \"include_upstream\":  false, \"include_downstream\":  false, \"include_future\":  false, \"include_past\":  false, \
  \"dag_run_id\": \"manual__2022-05-31T13:01:13.894084+00:00\", \
  \"new_state\": \"success\" }"

```
[explanation of above api](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html#operation/post_set_task_instances_state)

then the next step will execute.

concept is derived from [link](https://stackoverflow.com/questions/48580341/how-to-add-manual-tasks-in-an-apache-airflow-dag)

### 5th mid sized pipeline
- add aws conn string like this 
- ![image](https://betterdatascience.com/content/images/size/w1000/2022/03/2-32.png), [ref](https://betterdatascience.com/apache-airflow-amazon-s3-download/)
- I created a file s3://git-experiments/airflow-exp-p5-file-list.json
with contents
```
["plate_mh_p1.jpg", "rec_part2_p2.jpg", "survey_like_p2.png", "rec_appliance_p2.png", "rec_walmart_p1.jpg", "tax_us_p1.png"]
```

### graphiccal way via airflow 2.x issues
- [elyra on this link mentions that 'Apache Airflow version 2.x is currently not supported.'](https://github.com/elyra-ai/examples/tree/master/pipelines/run-generic-pipelines-on-apache-airflow)
- [cwl docs also talk about airflow 1.10 ui](https://cwl-airflow.readthedocs.io/en/latest/readme/how_to_use.html), pip install of  cwl-airflow in 2.x also failed
- so will stop attempts on 2.x and try on 1.x


### BPM type workflow?
- Using [Spiff](https://spiffworkflow.readthedocs.io/en/latest/intro.html) we can run user based workflow and standard bpmn diagrams. [Example project](https://github.com/sartography/spiff-example-cli) and somehow merge with airflow
- to view bpm https://demo.bpmn.io/

- to run
```
  859  git clone https://github.com/sartography/spiff-example-cli
  860  cd spiff-example-cli/
  861  sudo docker build . -t spiff_example_cli
  862  docker run -it --rm spiff_example_cli
```

### Things to try:
- [x] make json work
- [x] wait for human action though ui and then proceed with next task
- Generate dag using drawing
- drawing rules (priority codes, processs docments as per priority)
- parallel flow and merge (one that waits for manual)
> approve reject alternate flow
- queue - jira or library

### clean up
```
docker compose down --volumes --rmi all
```
# Airflow 1.9
using docker-compose version 1.27.4,
## Guides
- [Productionalizing Data Pipelines with Apache Airflow by Axel Sirota | Pluralsight](https://www.pluralsight.com/courses/productionalizing-data-pipelines-apache-airflow)
- [git study](https://github.com/mikeroyal/Apache-Airflow-Guide)
- [express youtube guide](https://www.youtube.com/watch?v=2v9AKewyUEo), [whose git is](https://github.com/soumilshah1995/Learn-Apache-Airflow-in-easy-way-/tree/main/project)

## Getting started project
[git productionalizing-data-pipelines-airflow](https://github.com/axel-sirota/productionalizing-data-pipelines-airflow)

## instructions to run the project
```
sudo docker-compose -f docker-compose19.yml build
sudo docker-compose -f docker-compose19.yml  up
```

## trigger run
### first run
- Hello world
- with hello_world.py
- docker-compose up
- view UI 
![image](https://user-images.githubusercontent.com/2136211/170428000-8b7c21cc-4f56-4686-9ed2-3b9caff12c80.png)
- Follow steps 1-6 to trigger the run and view logs
![image](https://user-images.githubusercontent.com/2136211/170429231-ea711094-42f3-4079-a8ee-aea6febfd3e2.png)

### file http mongo
- drop files into ./docker/airflow/fileinput folder to see fresh 30seconds polled based filesensor
- Create http connection (optional - if not done - right now python code is emulating it via airflow add connection command)
Admin>connections>add new and enter params like [this image](https://user-images.githubusercontent.com/2136211/170446792-def85dc5-34ef-410d-b48a-5569ad9395ba.png)
 - after starting http_rabbit dag
 - to test mongo insert run
 ```
sudo docker exec -it airflow-experiments_mongo_1 sh
# mongosh
test> show collections
postcollection
test> db.postcollection.count()
test> db.postcollection.find({}).take(1)
 ```
 - graph view
 ![image](https://user-images.githubusercontent.com/2136211/170595596-74e6bc06-e56f-4d99-9e0e-8c3b4c9e0b5a.png)
 - tree view
 ![image](https://user-images.githubusercontent.com/2136211/170595670-49fb902f-60cd-4160-b9a8-8b28806371c0.png)
- dag view
![image](https://user-images.githubusercontent.com/2136211/170596044-0814a79d-f01d-4f2e-a282-2b9121dc7269.png)



 ### API 
 - docs for 1.9/1.10 https://airflow.apache.org/docs/apache-airflow/1.10.3/api.html#endpoints
 - test http://localhost:8080/api/experimental/test from webbrowser
 - get latest run
 ```
 http://localhost:8080/api/experimental/latest_runs
 ```
- trigger dag run using api
```
curl -X POST \
  http://localhost:8080/api/experimental/dags/hello_world/dag_runs \
  -H 'Cache-Control: no-cache' \
  -H 'Content-Type: application/json' \
  -d '{"conf":"{\"key\":\"value\"}"}'
```
- pause a dag - http://localhost:8080/api/experimental/dags/hello_world/paused/true


## Rabbitmq operator issue
because for a few plugins - example rabbitmq - we run into [operator incomptibility](https://stackoverflow.com/questions/67233220/upgrading-to-airflow-2-no-module-named-airflow-hooks-base)



# Appendix

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


