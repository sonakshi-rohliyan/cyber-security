import os
import sys
import numpy as np 
import pandas as pd

TARGET_COLUMN = "Result"
PIPELINE_NAME = "src"
ARTIFACT_DIR = "Artifacts"
FILE_NAME = "phisingData.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema","schema.yaml")

# data ingestion starts here

DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_DATABASE_NAME = "MEOW"
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT = 0.2


# data validation starts here

DATA_VALIDATION_DIR_NAME:str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invvalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME:str = "report.yaml"

