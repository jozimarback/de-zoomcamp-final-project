resource "google_storage_bucket" "code" {
    name = "${var.data-project}-code-jozimar"
    force_destroy = false
    uniform_bucket_level_access = true
    location = var.region
}