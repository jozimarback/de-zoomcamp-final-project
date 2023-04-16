locals {
    labels = {
        "project" = var.project
    }
}

variable "project" {
    type= string
    description = "ID Google project"
}

variable "region" {
    type= string
    description = "Region Google project"
}

variable  "data-project" {
    type = string
    description = "Name data project"
}

variable  "kaggle-key" {
    type = string
    description = "Kaggle key user"
}

variable  "kaggle-username" {
    type = string
    description = "Kaggle user name"
}