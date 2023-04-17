data "google_compute_default_service_account" "default" {
    project = var.project
}
resource "google_cloud_scheduler_job" "avg-years-schooling" {
  name = "${var.data-project}-avg-years-schooling"
  description = "Average years of schooling"
  schedule = "5 4 1 * *"
  time_zone = "America/Sao_Paulo"
  retry_config {
    retry_count = 0
  }
  http_target {
    http_method = "POST"
    uri = google_cloudfunctions_function.trigger-dataproc-workflow.https_trigger_url
    oidc_token {
      service_account_email = data.google_compute_default_service_account.default.email
    }
    body = base64encode("{}")
  }
}