from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.components.model_trainer import ModelTrainer
import sys
if __name__=="__main__":
    try:
        logging.info("ENTERED THE TRY BLOCK")
        training_pipeline_config=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(training_pipeline_config)
        data_validation_config=DataValidationConfig(training_pipeline_config)
        data_transformation_config=DataTransformationConfig(training_pipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config)
        logging.info("INITIALIZING THE DATA INGESTION")
        something=data_ingestion.initiate_dataingestion()
        data_validation=DataValidation(something,data_validation_config)
        something2=data_validation.initiate()
        data_transformation=DataTransformation(data_transformation_config,something2)
        something3=data_transformation.initiate()
        model_trainer_config=ModelTrainerConfig(training_pipeline_config)
        model_trainer=ModelTrainer(something3,model_trainer_config)
        model_trainer.initiate()
    except Exception as e:
        raise CustomException(e,sys)