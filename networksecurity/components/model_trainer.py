from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException

import os
import sys
import mlflow

from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifact,DataTransformationArtifact

from networksecurity.utils.mainutils.utils import load_object,load_array_obj
from networksecurity.utils.mainutils.utils import save_object

from networksecurity.utils.mlutils.metric.classification_metric import get_classification_metric
from networksecurity.utils.mainutils.utils import evaluate_model
from networksecurity.utils.mlutils.model.estimator import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline


class ModelTrainer:
    def __init__(self,data_transformation_artifact=DataTransformationArtifact,model_trainer_config=ModelTrainerConfig):
        try:
            logging.info("ENTERED MODEL TRAINER")
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)
    #MLflow ek diary hai jo tumhare Machine Learning experiments 
    # ko automatically likhti rehti hai.
    def train_model(self,x_train,y_train,x_test,y_test):
        try:
            logging.info("TRAINING OF MODEL HAS BEEN STARTED")
            models={
                "LogisticRegression":LogisticRegression(verbose=0),
                "RandomForestClassifier":RandomForestClassifier(verbose=0),
                "AdaBoostClassifier":AdaBoostClassifier(),
                "DecisionTreeClassifier":DecisionTreeClassifier(),
                "GradientBoostClassifier":GradientBoostingClassifier(verbose=0),
                "SupportVectorClassifier":SVC(verbose=False),
                "XGBoostCLassifier":XGBClassifier(),
                "KNNClassifier":KNeighborsClassifier(),
                "CatBoostClassifier":CatBoostClassifier(verbose=0),
            }
            params={
                "LogisticRegression":{
                    "C": [0.01, 0.1, 1, 10],
                    "penalty": ["l2"],
                    "solver": ["lbfgs", "liblinear"]
                },
                "RandomForestClassifier":{
                    "n_estimators": [100, 200, 300],
                    "max_depth": [None, 10, 20, 30],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4]
                },
                "AdaBoostClassifier":{
                    "n_estimators": [50, 100, 200],
                    "learning_rate": [0.01, 0.1, 1]

                },
                "DecisionTreeClassifier":{
                    "criterion": ["gini", "entropy"],
                    "max_depth": [None, 5, 10, 20],
                    "min_samples_split": [2, 5, 10],
                    "min_samples_leaf": [1, 2, 4]
                },
                "GradientBoostClassifier":{
                    "n_estimators": [100, 200],
                    "learning_rate": [0.01, 0.1],
                    "max_depth": [3, 5],
                    "subsample": [0.8, 1.0]
                },
                "SupportVectorClassifier":{
                    "C": [0.1, 1, 10],
                    "kernel": ["linear", "rbf"],
                    "gamma": ["scale", "auto"]
                },
                "XGBoostCLassifier":{
                    "n_estimators": [100, 200],
                    "learning_rate": [0.01, 0.1],
                    "max_depth": [3, 5, 7],
                    "subsample": [0.8, 1.0],
                    "colsample_bytree": [0.8, 1.0]
                },
                "KNNClassifier":{
                    "n_neighbors": [3, 5, 7, 9],
                    "weights": ["uniform", "distance"],
                    "metric": ["euclidean", "manhattan"]
                },
                "CatBoostClassifier":{
                    "iterations": [100, 200],
                    "learning_rate": [0.01, 0.1],
                    "depth": [4, 6, 8]
                }
            }
            report_details=evaluate_model(x_train,y_train,x_test,y_test,models,params)
            best_model=None
            best_model_score=-1
            for model,metric in report_details.items():
                
                if metric["Test F1"]>best_model_score:
                    best_model_score=metric["Test F1"]
                    best_model=model
            if best_model_score<0.60:
                raise Exception("NO SUITABLE MODEL FOUND")
            print("BEST MODEL NAME IS:-",best_model)
            print("BEST MODEL SCORE",best_model_score)
            final_model=models[best_model]
            y_train_pred=final_model.predict(x_train)
            train_classification_metric=get_classification_metric(y_train,y_train_pred)
            y_test_pred=final_model.predict(x_test)
            test_classification_metric=get_classification_metric(y_test,y_test_pred)
            preprocessor=load_object(self.data_transformation_artifact.transformed__object_file_path)
            network_model=NetworkModel(preprocessor=preprocessor,model=final_model)
            os.makedirs(os.path.dirname(self.model_trainer_config.trained_model_file_path),exist_ok=True)
            save_object(self.model_trainer_config.trained_model_file_path,object=network_model)
            model_trainer_artifact=ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=train_classification_metric,
                test_metric_artifact=test_classification_metric
            )
            save_object("finalmodel/model.pkl",final_model)
            logging.info("MODEL TRAINING HAS BEEN COMPLETED")
            logging.info("RETURNING MODEL TRAINER ARTIFACT AFTER TRAINING")
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate(self)-> ModelTrainerArtifact:
        try:
            logging.info("INITIATING THE MODEL TRAINER")
            logging.info("READING THE TRANSFORMED DATA")
            train_data=self.data_transformation_artifact.transformed_train_file_path
            test_data=self.data_transformation_artifact.transformed_test_file_path
            logging.info("LOADING THE ARRAY OBJECT")
            train_arr=load_array_obj(train_data)
            test_arr=load_array_obj(test_data)
            logging.info("DIVIDING THE DATA INTO X_TRAIN,Y_TRAIN,X_TEST,Y_TEST")
            x_train=train_arr[:,:-1]
            y_train=train_arr[:,-1]
            x_test=test_arr[:,:-1]
            y_test=test_arr[:,-1]
            logging.info("ENTERING TRAIN MODEL FUNCTION")
            artifact=self.train_model(x_train,y_train,x_test,y_test)
            logging.info("RETURNING MODEL TRAININ ARTIFACT FINALLY")
            return artifact
        except Exception as e:
            raise CustomException(e,sys)
'''def track_mlflow(self,best_model,classification_metric):
        with mlflow.start_run():
            f1_score=classification_metric.f1
            precison_score=classification_metric.precision
            recall_score=classification_metric.recall
            accuracy_score=classification_metric.accuracy
            mlflow.log_metric("f1 score",f1_score)
            mlflow.log_metric("precision score",precison_score)
            mlflow.log_metric("recall score",recall_score)
            mlflow.log_metric("accuracy score",accuracy_score)
            mlflow.sklearn.log_model(best_model,"model")
'''


        