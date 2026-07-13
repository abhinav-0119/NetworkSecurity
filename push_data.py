import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()

url=os.getenv('MONGO_DB_URL')
print(url)

import certifi
ca=certifi.where()
"""When Python connects to a server over HTTPS or TLS/SSL, it needs to make sure the server is really who it claims to be.

For example, when your code connects to MongoDB Atlas:

Your Python Program
        │
        │ Secure TLS Connection
        ▼
MongoDB Atlas Server

The MongoDB Atlas server sends its SSL certificate to your Python program.

Python then checks:

✅ Is this certificate issued by a trusted Certificate Authority (CA)?
✅ Has the certificate expired?
✅ Does the certificate belong to the server I'm connecting to?

If all these checks pass, Python establishes a secure connection.

If not, you'll get an SSL verification error such as:

SSL: CERTIFICATE_VERIFY_FAILED
"""

import pandas as pd
import numpy as np
import pymongo

from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging


class Extract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)
    def csv_json(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise CustomException(e,sys)
    def insert_data(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.records=records

            self.mongo_client=pymongo.MongoClient(url)
            self.database = self.mongo_client[self.database]
            
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return(len(self.records))

        except Exception as e:
            raise CustomException(e,sys)
if __name__=='__main__':
    FILE_PATH="Network_Data\phisingData.csv"
    DATABASE="ABHINAVANAND"
    Collection="NetworkData"
    networkobj=Extract()
    records=networkobj.csv_json(file_path=FILE_PATH)
    print(records)
    no_of_records=networkobj.insert_data(records,DATABASE,Collection)
    print(no_of_records)
        