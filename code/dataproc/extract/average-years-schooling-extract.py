from pyspark.sql import SparkSession, functions as f
from pyspark.sql.types import *
from google.cloud import storage
from kaggle.api.kaggle_api_extend import KaggleApi

from requests.adapters import HTTPAdapter, Retry
import requests
import sys
import json
import os


__BUCKET_RAW = sys.argv[0]
os.environ["KAGGLE_USERNAME"] = sys.argv[1]
os.environ["KAGGLE_KEY"] = sys.argv[2]

if __name__ == "__main__":
    spark = (
        SparkSession.builder
        .appName("Average years schooling extract")
        .getOrCreate()
    )

    kaggle_json_dir = '/root/.kaggle/'
    if not os.path.exists(kaggle_json_dir):
        os.makedirs(kaggle_json_dir) 
    with open(f'{kaggle_json_dir}kaggle.json', 'w') as f:
        f.write(json.dumps({"username":sys.argv[1],"key":sys.argv[2]}))
    os.chmod(f'{kaggle_json_dir}kaggle.json', 600)  

    api = KaggleApi()
    api.authenticate()
    file = "mean-years-of-schooling-long-run.csv"
    api.dataset_download_file("fredericksalazar/average-years-of-schooling-since-1870-2017",
                                file)

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(__BUCKET_RAW)
    blob = bucket.blob(f'csv/{file}')
    blob.upload_from_filename(file)