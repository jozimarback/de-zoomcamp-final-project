resource "google_storage_bucket_object" "dataproc-code" {
  for_each = fileset("../code/dataproc", "**/*")

  name = "dataproc/${each.value}"
  bucket = google_storage_bucket.code.name
  source = "../code/dataproc/${each.value}"
}

resource "google_storage_bucket_object" "bootstrap" {
  name = "dataproc/bootstrap.sh"
  bucket = google_storage_bucket.code.name
  content = templatefile("bootstrap.template", {
    bucket = google_storage_bucket.code.name
  })
}


resource "google_dataproc_workflow_template" "dataproc-average-years-schooling" {
  name = "${var.data-project}-avg-years-schooling"
  dag_timeout = "${60 * 60}s" # 1 hour
  location = var.region
  labels = local.labels
  placement {
    managed_cluster {
      cluster_name = "${var.data-project}-avg-years-schooling"
      config {
        staging_bucket = google_storage_bucket.tmp-dataproc.name
        temp_bucket = google_storage_bucket.tmp-dataproc.name
        initialization_actions {
          executable_file = "gs://${google_storage_bucket.code.name}/dataproc/bootstrap.sh"
        }
        endpoint_config {
          enable_http_port_access = true
        }
        software_config {
          image_version = "2.0"
          properties = {
            "spark:spark.jars" = "gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.25.2.jar"
            "spark:spark.sql.sources.partitionOverwriteMode" = "dynamic"
            "spark:spark.dynamicAllocation.enabled" = "true"
          }
        }
        gce_cluster_config {
          zone = ""
          internal_ip_only = false
          service_account_scopes = [
            "https://www.googleapis.com/auth/cloud-platform"
          ]
        }
        master_config {
          num_instances = 1
          machine_type = "n1-standard-2"
          disk_config {
            boot_disk_type = "pd-standard"
            boot_disk_size_gb = 50
          }
        }
        worker_config {
          num_instances = 2
          machine_type = "n1-standard-2"
          disk_config {
            boot_disk_type = "pd-standard"
            boot_disk_size_gb = 50
          }
        }
      }
    }
  }
  jobs {
    step_id = "average-years-schooling-extract-setup"
    pyspark_job {
      main_python_file_uri = "gs://${google_storage_bucket.code.name}/dataproc/extract/average-years-schooling-extract-setup.py"
      args = [
            var.kaggle-username
            ,var.kaggle-key
      ]
    }
  }
  jobs {
    step_id = "average-years-schooling-extract"
    prerequisite_step_ids = ["average-years-schooling-extract-setup"]
    pyspark_job {
      main_python_file_uri = "gs://${google_storage_bucket.code.name}/dataproc/extract/average-years-schooling-extract.py"
      args = [
            google_storage_bucket.raw.name
            ,var.kaggle-username
            ,var.kaggle-key
      ]
    }
  }
  jobs {
    step_id = "average-years-schooling-load"
    prerequisite_step_ids = ["average-years-schooling-extract"]
    pyspark_job {
      main_python_file_uri = "gs://${google_storage_bucket.code.name}/dataproc/load/average-years-schooling-load.py"
      args = [
          google_storage_bucket.raw.name
          ,google_storage_bucket.tmp-dataproc.name
          ,google_bigquery_dataset.kaggle.project
          ,google_bigquery_dataset.kaggle.dataset_id
          ,google_bigquery_table.tb_average_years_schooling.table_id
      ]
    }
  }  
}

