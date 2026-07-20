import yaml
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
#import dill
import pickle
from sklearn.metrics import accuracy_score,recall_score,precision_score,f1_score
from sklearn.model_selection import GridSearchCV
def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e, sys) from e
    
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise CustomException(e, sys)
def save_array_obj(file_path:str,array:np.array):
    try:
        logging.info("ENTERED FOR SAVING THE ARRAY OBJECT")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
        logging.info("EXITING FOR SAVING THE ARRAY OBJECT")
    except Exception as e:
        raise CustomException(e,sys)
def save_object(file_path:str,object):
    try:
        logging.info("ENTERED FOR SAVING THE PREPROCESSOR OBJECT")
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(object,file_obj)
        logging.info("EXITED AFTER SAVING PREPROECESSOR OBJECT")
    except Exception as e:
        raise CustomException(e,sys)
    
def load_object(file_path):
    try:
        with open(file_path,"rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)
    

def load_array_obj(file_path:str)-> np.array:
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
        logging.info("EXITING FOR LOADING THE ARRAY OBJECT")
    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_model(x_train,y_train,x_test,y_test,models:dict,params):
    try:
        report={}
        model_keys=list(models.keys())
        model_values=list(models.values())
        for i in range(len(list(models))):
            model=model_values[i]
            gs=GridSearchCV(estimator=model,param_grid=params[model_keys[i]],cv=5,n_jobs=-1,scoring="f1")
            gs.fit(x_train,y_train)
            model.set_params(**gs.best_params_)
            model.fit(x_train,y_train)
            y_train_pred=model.predict(x_train)
            y_test_pred=model.predict(x_test)

            report[model_keys[i]]={
                "Train Accuracy": accuracy_score(y_train, y_train_pred),
                "Test Accuracy": accuracy_score(y_test, y_test_pred),

                "Train Precision": precision_score(y_train, y_train_pred),
                "Test Precision": precision_score(y_test, y_test_pred),

                "Train Recall": recall_score(y_train, y_train_pred),
                "Test Recall": recall_score(y_test, y_test_pred),

                "Train F1": f1_score(y_train, y_train_pred),
                "Test F1": f1_score(y_test, y_test_pred),
            }
        return report
    except Exception as e:
        raise CustomException(e,sys)

        
