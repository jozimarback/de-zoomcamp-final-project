from pyspark.sql import SparkSession
from pyspark.sql.types import *
from google.cloud import storage
import os
import sys

from kaggle.api.kaggle_api_extended import KaggleApi
import logging


__BUCKET_RAW = sys.argv[1]

def extract_kaggle_dataset(file):  
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_file("fredericksalazar/average-years-of-schooling-since-1870-2017",
                                file)

def send_file_to_raw_bucket(file):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(__BUCKET_RAW)
    blob = bucket.blob(f'csv/{file}')
    blob.upload_from_filename(file)

if __name__ == "__main__":
    spark = (
        SparkSession.builder
        .appName("Average years schooling extract")
        .getOrCreate()
    )

    file = "mean-years-of-schooling-long-run.csv"
    if not os.path.isfile('/root/.kaggle/kaggle.json'):
        logging.error("File kaggle.json does not exist")
    extract_kaggle_dataset(file)
    send_file_to_raw_bucket(file)