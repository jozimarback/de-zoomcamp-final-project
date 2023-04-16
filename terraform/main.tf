terraform {
    backend "gcs" { 
      bucket  = "terraform-state-jozimar-de-zoocamp"
      prefix  = "prod"
    }
}

provider "google" {
  project = var.project
  region = var.region
}