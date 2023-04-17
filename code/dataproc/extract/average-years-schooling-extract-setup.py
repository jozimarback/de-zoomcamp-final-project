import logging
from pyspark.sql import SparkSession
import json
import os
import sys

def create_kaggle_auth_file():
    kaggle_json_dir = '/root/.kaggle'
    if not os.path.exists(kaggle_json_dir):
        os.makedirs(kaggle_json_dir) 
    with open(f'{kaggle_json_dir}/kaggle.json', 'w') as f:
        json.dump({"username":sys.argv[1], "key":sys.argv[2]}, f)
    os.chmod(f'{kaggle_json_dir}/kaggle.json', 600)
    logging.info('Created kaggle file')

if __name__ == "__main__":
    spark = (
        SparkSession.builder
        .appName("Average years schooling extract setup")
        .getOrCreate()
    )
    create_kaggle_auth_file()   