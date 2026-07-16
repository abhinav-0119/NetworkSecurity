import yaml
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
import os,sys
import numpy as np
#import dill
import pickle
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