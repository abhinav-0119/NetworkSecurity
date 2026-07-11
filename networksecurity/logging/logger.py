import logging
from datetime import datetime
import os


log_file=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" # NAME OF LOG FILE
log_path=os.path.join(os.getcwd(),"logs") #MAKING FOLDER NAMED "LOGS" IN CURRENT DIRECTORY
os.makedirs(log_path,exist_ok=True)
log_file_path=os.path.join(log_path,log_file)# LOG_FILE INSIDE LOG_PATH

#BELOW IS SETUP OF LOGGING
logging.basicConfig(
    filename=log_file_path,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)