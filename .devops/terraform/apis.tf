provider "google" {
  project = var.gc_project_id
  region  = var.region
}

resource "google_project_service" "iam" {
  provider           = google-beta
  service            = "iam.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "artifactregistry" {
  provider           = google-beta
  service            = "artifactregistry.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloudrun" {
  provider           = google-beta
  service            = "run.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "resourcemanager" {
  provider           = google-beta
  service            = "cloudresourcemanager.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "cloudbuild" {
  provider           = google-beta
  service            = "cloudbuild.googleapis.com"
  disable_on_destroy = false
}

resource "time_sleep" "wait_30_seconds" {
  create_duration = "30s"
  depends_on = [
    google_project_service.iam,
    google_project_service.artifactregistry,
    google_project_service.cloudrun,
    google_project_service.resourcemanager,
    google_project_service.cloudbuild,
  ]
}