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
}

provider "google-beta" {
  project = var.gc_project_id
  region  = var.region
  zone    = var.zone
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
  registry_auth {
    address = "${var.region}-docker.pkg.dev"
    config_file = pathexpand("~/.docker/config.json")
  }
}