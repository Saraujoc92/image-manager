terraform {
  required_providers {
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "6.36.1"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.6.0"
    }
  }
  backend "gcs" {
    bucket = "image_manager_api_terraform_state_bucket"
    prefix = "terraform/state"
  }
}

provider "google-beta" {
  project = var.gc_project_id
  region  = var.region
  zone    = var.zone
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
  registry_auth {
    address     = "${var.region}-docker.pkg.dev"
    config_file = pathexpand("~/.docker/config.json")
  }
}
