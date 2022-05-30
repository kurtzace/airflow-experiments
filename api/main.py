from typing import Union

from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
app = FastAPI()
client=MongoClient("mongodb://mongo:27017/")
db=client['test']
coll=db['allot']



@app.get("/health")
def health():
    return {"status": True}

@app.get("/allhumanstatus")
def allstatus():
    return coll.find({})

@app.get("/gethumanstatus/{jobid}")
def gethumanstatus(jobid: str):
    specific=coll.find_one({'JobId':jobid})
    if("Status" in specific):
        return specific["Status"]
    else:
        return "pending"

@app.get("/save/{jobid}")
def save(jobid: str):
    coll.insert_one({'JobId':jobid})
    return {'status':'ok'}

@app.get("/sethumaninput/{db_id}")
def approve(db_id: str, status: bool):
    coll.update_many({"JobId":db_id}, {'$set':{'Status': status}})
    return {"db_id": db_id, "status": status}
