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