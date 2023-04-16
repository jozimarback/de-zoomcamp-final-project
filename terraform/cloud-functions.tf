data "archive_file" "trigger-dataproc-workflow-code-zip" {
    type = "zip"
    source_dir = "../code/cloudfunction/trigger-dataproc-workflow"
    output_path = "cloudfunction/trigger-dataproc-workflow"
}

resource "google_storage_bucket_object" "trigger-dataproc-workflow-code" {
    name = "${data.archive_file.trigger-dataproc-workflow-code-zip.name}-${data.archive_file.trigger-dataproc-workflow-code-zip.output_sha}.zip"
    buket = google_storage_bucket.code.name
    source = data.archive_file.trigger-dataproc-workflow-code-zip.output_path
}

resource "google_cloudfunctions_function" "trigger-dataproc-workflow" {
  name = "${var.data-project}-trigger-dataproc-workflow"
  runtime = "python38"
  entry_point = "main"
  trigger_http = true
  available_memory_mb = 256
  source_archive_bucket = google_storage_bucket.code.name
  source_archive_object = google_storage_bucket_object.trigger-dataproc-workflow-code.name
  environment_variables = {
    "REGION" = var.region
    "PROJECT_ID" = var.project
    "DATAPROC_WORKFLOW" = google_dataproc_workflow_template.dataproc_average_years_schooling.name
  }
}