from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException
import sys
from src.logger import logging
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig
from src.entity.config_entity import TrainingPipelineConfig

if __name__ == "__main__":
    try:

        # data ingestion
        training = TrainingPipelineConfig()
        data_ingestion_confi = DataIngestionConfig(training)
        data_ingestion = DataIngestion(data_ingestion_confi)
        logging.info("Initiate module")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data initiation completed")
        print(data_ingestion_artifact)

        # data validation
        data_validation_config = DataValidationConfig(training)
        data_validate = DataValidation(data_ingestion_artifact,data_validation_config)
        logging.info("initiate data validation")
        data_validation_artifact = data_validate.initiate_data_validation()
        logging.info("finished the data validation")
        print(data_validation_artifact)

        # data transformation
        data_transformation_config = DataTransformationConfig(training)
        data_transformation = DataTransformation(data_validation_artifact,data_transformation_config)
        logging.info("initiate data transformation")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("finished the data transformation")
        print(data_transformation_artifact)

        # model trainer config
        model_trainer_config = ModelTrainerConfig(training)
        model_trainer = ModelTrainer(model_trainer_config,data_transformation_artifact)
        logging.info("Meow meow model training")
        model_trainer_arti = model_trainer.initiate_model_trainer()
        logging.info("Model training artifact create")
        print(model_trainer_arti)

    except Exception as e:
        raise CustomException(e,sys)

