import os
import sys

import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from src.exception import CustomException
from src.logger import logging
from src.constants import training_pipeline
from src.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from src.entity.config_entity import DataTransformationConfig
from src.utils import save_numpy_array_data,save_object


class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, data_transformation_config: DataTransformationConfig):
        try:
           self.data_validation_artifact = data_validation_artifact
           self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise CustomException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)
        
    def data_transforming_pipeline(cls) -> Pipeline:
        '''
        It initialises a KNNImputer object with the parameters speciied in the training_pipeline.py
        It uses KNN imputers, who's job is to fill in the nan values
        '''
        logging.info("Entered data_transforming_pipeline to form a pipelinne")
        try:
            imputer = KNNImputer(**training_pipeline.DATA_TRANSFORMATION_IMPUTER_PARAMS)
            processor = Pipeline([("imputer",imputer)])

            return processor
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation in DataTransformation class")
        try:
            logging.info("Starting data tranformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            # training dataframe
            input_feature_train_df = train_df.drop(columns=[training_pipeline.TARGET_COLUMN])
            output_feature_train_df = train_df[training_pipeline.TARGET_COLUMN]
            output_feature_train_df = output_feature_train_df.replace(-1,0)

            # test dataframe
            input_feature_test_df = test_df.drop(columns=[training_pipeline.TARGET_COLUMN])
            output_feature_test_df = test_df[training_pipeline.TARGET_COLUMN]
            output_feature_test_df = output_feature_test_df.replace(-1,0)

            #implementing knn imputer
            processor = self.data_transforming_pipeline()

            preprocessor_obj = processor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_obj.transform(input_feature_train_df)
            tranformed_input_test_feature = preprocessor_obj.transform(input_feature_test_df)

            # now we'll combine our tranformed input array with the output

            train_arr = np.c_[transformed_input_train_feature,np.array(output_feature_train_df)]
            test_arr = np.c_[tranformed_input_test_feature, np.array(output_feature_test_df)]

            # now we save the funtion
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_obj)

            # preparing thee artifact
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)