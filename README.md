# Data Engineer Zoomcamp Final Project

This project is a data engineering pipeline with data about education around the world in more than 100 years of history from Kaggle dataset. 

Education is widely accepted to be a fundamental resource, both for individuals and societies. Indeed, in most countries basic education is nowadays perceived not only as a right, but also as a duty – governments are typically expected to ensure access to basic education, while citizens are often required by law to attain education up to a certain basic level.

The data on the production of education shows that schooling tends to be largely financed with public resources across the globe, although a great deal of heterogeneity is observed between countries and world regions.

## Dataset

The [kaggle dataset](https://www.kaggle.com/datasets/fredericksalazar/average-years-of-schooling-since-1870-2017) contains information about the average years of schooling since 1870 to 2017 in countries around the world. The source of kaggle dataset DataSet is downloaded from https://ourworldindata.org/global-education.

### Pipeline

![pipeline](./docs/pipeline.png)

The pipeline starts with a cloud scheduler cron witch trigger a cloud function.

Inside the cloud function there is a logic to call a dataproc workflow that processes a ETL over data collected from kaggle dataset. The ETL process stores raw data(csv) in the cloud storage and ingest the csv file into BigQuery.

A dashboard was created with the data stored in BigQuery partitioned by year.

### Dashboard

In the dashboard we are able to filter by year and average year of schooling. We can also filter by country selecting countries on the map.
[Link](https://lookerstudio.google.com/reporting/95836a41-cbea-4e48-8ebf-202f89b22f34/page/wF8MD)
![report-1](./docs/report-1.png)

To reproduce this project you can use github actions.
Learn more [here on my blog](https://jozimarback.medium.com/using-github-actions-with-terraform-on-gcp-d473a37ddbd6)
