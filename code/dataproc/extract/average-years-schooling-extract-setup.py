import json
import logging
import os
from pyspark.sql import SparkSession
from pathlib import Path
import sys

def create_kaggle_auth_file():
    kaggle_json_dir = '/root/.kaggle'
    os.makedirs(kaggle_json_dir, exist_ok=True)
    with open(f'{kaggle_json_dir}/kaggle.json', 'w') as file:
        json.dump({'username':sys.argv[1],'key':sys.argv[2]}, file)
    os.chmod(f'{kaggle_json_dir}/kaggle.json', 600)
   
    if not os.path.isfile('/root/.kaggle/kaggle.json'):
        logging.error("File kaggle.json does not exist")
    else:
        print('Created kaggle file')
        logging.info('Created kaggle file')

if __name__ == "__main__":
    spark = (
        SparkSession.builder
        .appName("Average years schooling extract setup")
        .getOrCreate()
    )
    create_kaggle_auth_file()   