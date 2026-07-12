from src.components.data_ingestion import DataIngestion
from src.exception import CustomException
import sys
from src.logger import logging
from src.components.data_validation import DataValidation
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig
from src.entity.config_entity import TrainingPipelineConfig

if __name__ == "__main__":
    try:
        training = TrainingPipelineConfig()
        data_ingestion_confi = DataIngestionConfig(training)
        data_ingestion = DataIngestion(data_ingestion_confi)
        logging.info("Initiate module")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data initiation completed")
        print(data_ingestion_artifact)
        data_validation_config = DataValidationConfig(training)
        data_validate = DataValidation(data_ingestion_artifact,data_validation_config)
        logging.info("initiate data ingestion")
        data_validation_artifact = data_validate.initiate_data_validation()
        logging.info("finished the data validation")
        print(data_validation_artifact)

    except Exception as e:
        raise CustomException(e,sys)

