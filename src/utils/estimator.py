from src.constants.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
from src.exception import CustomException

import os
import sys

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            CustomException(e,sys)

    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_value = self.model.predict(x_transform)
            return y_value
        except Exception as e:
            CustomException(e,sys)