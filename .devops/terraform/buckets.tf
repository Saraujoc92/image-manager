
resource "google_storage_bucket" "image_upload_bucket" {
  name = var.image_upload_bucket_name
  location = var.region
  uniform_bucket_level_access = true
  versioning {
    enabled = false
  }
  force_destroy = true
}

resource "google_storage_bucket_iam_member" "api_sa_img_bucket_access" {
  bucket = google_storage_bucket.image_upload_bucket.name
  role   = "roles/storage.objectUser"
  member = "serviceAccount:${google_service_account.api_service_account.email}"
}

resource "google_storage_bucket" "logs_bucket" {
  name = var.logger_bucket_name
  location = var.region
  uniform_bucket_level_access = true
  versioning {
    enabled = false
  }
  force_destroy = true
}

resource "google_storage_bucket_iam_member" "api_sa_logs_bucket_access" {
  bucket = google_storage_bucket.logs_bucket.name
  role   = "roles/storage.objectUser"
  member = "serviceAccount:${google_service_account.api_service_account.email}"
}