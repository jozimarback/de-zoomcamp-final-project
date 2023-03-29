from pyspark.sql import SparkSession, functions as f
from pyspark.sql.types import *
from google.cloud import storage
import kaggle
from kaggle.api.kaggle_api_extend import KaggleApi

from requests.adapters import HTTPAdapter, Retry
import requests

if __name__ == "__main__":
    # session = requests.session()
    # session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.178 Safari/537.36'})
    # retry = Retry(connect=3, backoff_factor=0.5)
    # adapter = HTTPAdapter(max_retries=retry)
    # session.mount('http://', adapter)
    # session.mount('https://', adapter)
    # session.get()
    api = KaggleApi()
    api.authenticate()
    file = "mean-years-of-schooling-long-run.csv"
    api.dataset_download_file("fredericksalazar/average-years-of-schooling-since-1870-2017",
                                file)

    storage_client = storage.Client()
    bucket = storage_client.get_bucket('bucket-destino...')
    blob = bucket.blob(f'RAW/{file}')
    blob.upload_from_filename(file)