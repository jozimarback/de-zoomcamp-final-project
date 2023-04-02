from pyspark.sql import SparkSession, functions as f
from pyspark.sql.types import *
from google.cloud import storage
import kaggle
from kaggle.api.kaggle_api_extend import KaggleApi

from requests.adapters import HTTPAdapter, Retry
import requests
import sys

__BUCKET_RAW = sys.argv[0]

if __name__ == "__main__":
    spark = (
        SparkSession.builder
        .appName("Average years schooling extract")
        .getOrCreate()
    )
    api = KaggleApi()
    api.authenticate()
    file = "mean-years-of-schooling-long-run.csv"
    api.dataset_download_file("fredericksalazar/average-years-of-schooling-since-1870-2017",
                                file)

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(__BUCKET_RAW)
    blob = bucket.blob(f'csv/{file}')
    blob.upload_from_filename(file)