from src.components.data_ingestion import DataIngestion
from src.exception import CustomException
import sys
from src.logger import logging
from src.entity.config_entity import DataIngestionConfig
from src.entity.config_entity import TrainingPipelineConfig

if __name__ == "__main__":
    training = TrainingPipelineConfig()
    data_ingestion_confi = DataIngestionConfig(training)
    data_ingestion = DataIngestion(data_ingestion_confi)
    logging.info("Initiate module")

    dartifact = data_ingestion.initiate_data_ingestion()
    print(dartifact)

