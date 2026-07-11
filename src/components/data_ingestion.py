import os
import sys
from typing import List

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import pymongo

from src.exception import CustomException
from src.logger import logging

#import the config of data Ingestion
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestArtifact

# import our mongodb database
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config :DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)
        
    def export_collection_as_df(self):
        '''
        Read data from mongodb and convert it to dataframe
        '''
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]

            logging.info("Sucessfully connected")
            df = pd.DataFrame(list(collection.find()))

            logging.info("Dataframe created from MongoDb")

            if "_id" in df.columns.to_list():
                df = df.drop(columns = ["_id"])

            df.replace({"na":np.nan},inplace=True)
            return df

        except Exception as e:
            raise CustomException(e,sys)
        
    def export_data_into_feature_store(self,dataframe: pd.DataFrame):
        '''
        Converts the dataframe that we got from the previous function into a csv file for future use
        '''
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            dataframe.to_csv(feature_store_file_path,index=False,header=True)

            logging.info("csv file created in the location using dataframe")
            
            return dataframe
        
        except Exception as e:
            raise CustomException(e,sys)

    def split_data_as_train_test(self, dataframe):
        try:
            train_set,test_set = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on dataframe")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_set.to_csv(self.data_ingestion_config.training_file_path, index = False, header = True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index = False, header = True)

            logging.info("Train and Test csv created")
            
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_ingestion(self):
        try:
            df = self.export_collection_as_df()
            df = self.export_data_into_feature_store(df)
            self.split_data_as_train_test(df)

            Data_ingestion_artifact = DataIngestArtifact(trained_file_path = self.data_ingestion_config.training_file_path , test_file_path = self.data_ingestion_config.testing_file_path)

            return Data_ingestion_artifact

        except Exception as e:
            raise CustomException(e,sys)        