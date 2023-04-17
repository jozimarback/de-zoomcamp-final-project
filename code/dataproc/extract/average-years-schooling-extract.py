from pyspark.sql import SparkSession
from pyspark.sql.types import *
from google.cloud import storage
import os
import sys

from kaggle.api.kaggle_api_extended import KaggleApi
import logging


__BUCKET_RAW = sys.argv[1]

def extract_kaggle_dataset(file_name:str)->None:
    """Download kaggle dataset

    Args:
        file_name (str): Filename of the dataset
    """
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_file("fredericksalazar/average-years-of-schooling-since-1870-2017",
                                file_name)

def send_file_to_raw_bucket(file_name:str)->None:
    """Send file to raw bucket GCP

    Args:
        file_name (str): File name to send to
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(__BUCKET_RAW)
    blob = bucket.blob(f'csv/{file_name}')
    blob.upload_from_filename(file_name)

if __name__ == "__main__":
    spark = (
        SparkSession.builder
        .appName("Average years schooling extract")
        .getOrCreate()
    )

    file_name = "mean-years-of-schooling-long-run.csv"
    if not os.path.isfile('/root/.kaggle/kaggle.json'):
        logging.error("File kaggle.json does not exist")
    extract_kaggle_dataset(file_name)
    send_file_to_raw_bucket(file_name)