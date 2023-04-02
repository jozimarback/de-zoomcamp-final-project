resource "google_bigquery_dataset" "kaggle" {
  project = var.projeto-dados
  dataset_id = "kaggle"
  description = "Kaggle extraction"
  labels = local.labels
}


resource "google_bigquery_table" "tb_average_years_schooling" {
  project = var.projeto-dados
  dataset_id = google_bigquery_dataset.kaggle.dataset_id
  table_id  = "tb_average_years_schooling"
  description = "Average years of Schooling"
  schema = <<SCHEMA
  [
    {
        "name": "entity",
        "description": "name of country",
        "type": "STRING"
    },
    {
        "name": "code",
        "description": "Alpha-3 code country",
        "type": "STRING"
    },
    {
        "name": "avg_years_of_schooling",
        "description": "Average of years of schooling",
        "type": "FLOAT64"
    },
    {
        "name": "year",
        "description": "Year of medition",
        "type": "INTEGER"
    },
  ]
SCHEMA
  range_partitioning {
    field = "year"
    range {
      start = 1800
      end = 2500
      interval = 1
    }
  }
  labels = local.labels
}
