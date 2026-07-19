import sys
import os 

import pymongo
import certifi
c = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
print(mongo_db_url)

from src.exception import CustomException
from src.logger import logging
from src.pipeline.training_pipeline import TrainingPipeline
from src.constants import training_pipeline

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse

import pandas as pd
 
from src.utils import load_object

client = pymongo.MongoClient(mongo_db_url, tlsCAFile= c)

database = client[training_pipeline.DATA_INGESTION_DATABASE_NAME]
collection = database[training_pipeline.DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipe = TrainingPipeline()
        train_pipe.run_pipeline()
        return Response("Training is successful")
    except Exception as e:
        raise CustomException(e,sys)
    

if __name__ == "__main__":
    app_run(app,host="localhost",port=8000)