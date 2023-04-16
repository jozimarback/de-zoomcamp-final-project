resource "google_storage_bucket" "code" {
    name = "${var.data-project}-code-jozimar"
    force_destroy = false
    uniform_bucket_level_access = true
    location = var.region
}

resource "google_storage_bucket" "tmp-dataproc" {
  name = "${var.data-project}-tmp-dataproc"
  force_destroy = false
  uniform_bucket_level_access = true
  labels = local.labels
  location = var.regiao
  lifecycle_rule {
    condition {
      age = 30
    }
    action {
      type = "Delete"
    }
  }
}