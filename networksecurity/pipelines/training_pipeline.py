import os
import sys

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.constants.training_pipeline import TRAINING_BUCKET_NAME

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.cloud.s3_syncer import S3Sync


from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.entity.artifact_entity import DataTransformationArtifact
from networksecurity.entity.artifact_entity import DataValidationArtifact
from networksecurity.entity.artifact_entity import ModelTrainerArtifact

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_dataingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)
    def start_data_validation(self):
        try:
            self.data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation=DataValidation(data_ingestion_artifact=self.data_ingestion_artifact,data_validation_config=self.data_validation_config)
            data_validation_artifact=data_validation.initiate()
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e,sys)
    def start_data_transformation(self):
        try:
            self.data_transformation_config=DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation=DataTransformation(data_transformation_config=self.data_transformation_config,data_validation_artifact=self.data_validation_artifact)
            data_transformation_artifact=data_transformation.initiate()
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)
    def start_model_trainer(self):
        try:
            self.model_trainer_config=ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer=ModelTrainer(data_transformation_artifact=self.data_transformation_artifact,data_ingestion_config=self.data_ingestion_config)
            model_trainer_artifact=model_trainer.initiate()
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)
