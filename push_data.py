# we will read our data convert it to json and push it to mongodb

import os
import sys
import json

from dotenv import load_dotenv
import certifi
import pymongo

import pandas as pd
import numpy as np

from src.exception import CustomException
from src.logger import logging

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi
ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)

    def csv_to_json(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            '''
            to convert it to list of json we need to get the transpose of the data
            for example rn our data looks smth like
            A B C 
            1 1 0 
            1 0 1 
            our json should look smth like
            [{A:1,B:1,C:0},{A:1,B:1,C:0}]
            here each element is a json
            '''
            records = list(json.loads(data.T.to_json()).values())
            logging.info("Converted data to json")
            return records
        except Exception as e:
            raise CustomException(e,sys)
        
    def insert_data_to_mongo(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            logging.info("Pushed json to mongodb")
            return(len(self.records))
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == "__main__":
    FILE_PATH = "Network_data/phisingData.csv"
    DATABASE = "MEOW"
    Collection = "NetworkData"
    net_obj = NetworkDataExtract()
    record = net_obj.csv_to_json(file_path=FILE_PATH)
    no_records = net_obj.insert_data_to_mongo(records=record,database=DATABASE,collection=Collection)
    print(no_records)