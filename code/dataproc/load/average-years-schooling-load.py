from pyspark.sql import SparkSession, functions as f
from pyspark.sql.types import *
import sys

__BUCKET_RAW = sys.argv[1]
__TMP_BUCKET = sys.argv[2]
__TABLE = f"{sys.argv[3]}.{sys.argv[4]}.{sys.argv[5]}"

if __name__ == "__main__":
    spark = (
        SparkSession.builder
        .appName("Average years schooling load")
        .getOrCreate()
    )

    (
        spark.read
            .option("inferSchema",True)
            .option("header",True)
            .option("delimiter",';')
            .csv(f"gs://{__BUCKET_RAW}/csv/*.csv")
            .write.format("bigquery")
                    .mode('overwrite')
                    .option("table", __TABLE)
                    .option("temporaryGcsBucket", __TMP_BUCKET)
                    .save()
    )