from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException

import sys
import os
import pandas as pd
import numpy as np

from networksecurity.entity.artifact_entity import DataValidationArtifact
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from networksecurity.constants.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAM
from networksecurity.utils.mainutils.utils import save_object,save_array_obj


class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,data_validation_artifact:DataValidationArtifact):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise CustomException(e,sys)
    def read_data(file_path):
        try:
            df=pd.read_csv(file_path)
            return df

        except Exception as e:
            raise CustomException(e,sys)
    def get_preprocessor():
        try:
            # since all are numerical features so we dont have to make preprocessing pipeline for 
            # categorical features
            preprocessor=Pipeline(
                steps=[
                ("imputer",KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAM))
                ]
            )
            return preprocessor
        except Exception as e :
            raise CustomException(e,sys)
    def initiate(self)-> DataTransformationArtifact:
        try:
            train_file_path=self.data_validation_artifact.valid_train_file_path
            test_file_path=self.data_validation_artifact.valid_test_file_path
            logging.info("READING THE TRAINING AND TESTING DATA FOR TRANSFORMATION")
            train_df=DataTransformation.read_data(train_file_path)
            test_df=DataTransformation.read_data(test_file_path)
            print(train_df)
            logging.info("READING OF TRAINING AND TESTING DATA FOR TRANSFORMATION HAS BEEN COMPLETED")
            logging.info("DIVIDING INPUT AND TRAGET FEATURES FOR TRAIN AND TEST DATA")
            train_target_feature=train_df[TARGET_COLUMN]
            train_input_feature=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            train_target_feature = train_target_feature.replace(-1, 0)
            test_target_feature=test_df[TARGET_COLUMN]
            test_input_feature=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            test_target_featuredf = test_target_feature.replace(-1, 0)
            logging.info("DIVIDING INPUT AND TRAGET FEATURES FOR TRAIN AND TEST DATA COMPLETED")
            preprocessor=DataTransformation.get_preprocessor()
            transformed_train_input_feature=preprocessor.fit_transform(train_input_feature)
            transformed_test_input_feature=preprocessor.transform(test_input_feature)
            print(type(train_target_feature))
            print(type(transformed_train_input_feature))
            train_array=np.c_[transformed_train_input_feature,np.array(train_target_feature)]
            test_array=np.c_[transformed_test_input_feature,np.array(test_target_feature)]
            train_data=save_array_obj(self.data_transformation_config.transformed_train_data_file_path,train_array)
            test_data=save_array_obj(self.data_transformation_config.transformed_test_data_file_path,test_array)
            save_object(
                self.data_transformation_config.preprocessor_obj_file_path,preprocessor
            )
            data_transformation_artifact=DataTransformationArtifact(
                self.data_transformation_config.transformed_train_data_file_path,
                self.data_transformation_config.transformed_test_data_file_path,
                self.data_transformation_config.preprocessor_obj_file_path
            )
            logging.info("RETURNING DATA TRANSFORMATION ARTIFACT")
            logging.info("DATA TRANSFORMATION HAS BEEN COMPLETED")
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)

        





