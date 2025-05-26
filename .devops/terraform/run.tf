resource "docker_registry_image" "api_image" {
  name = "${var.region}-docker.pkg.dev/${var.gc_project_id}/${var.repository}/${var.docker_image}"
  
  depends_on = [
    module.gcloud,
    google_artifact_registry_repository_iam_member.docker_pusher_iam
  ]
}

resource "google_cloud_run_service" "image_manager_app" {
  provider = google-beta
  name     = var.docker_image
  location = var.region
  template {
    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "0"
        "autoscaling.knative.dev/maxScale" = "1"
      }
      labels = {
        "env" : "dev"
      }
    }
    spec {
      containers {
        image = "${docker_registry_image.api_image.name}@${docker_registry_image.api_image.sha256_digest}"
        env { 
            name  = "DATABASE_URL"
            value ="postgresql://${var.db_username}:${var.db_password}@${google_sql_database_instance.image_manager_db.public_ip_address}:5432/${var.db_instance_name}"
        }
        env {
            name  = "IMAGE_UPLOAD_BUCKET"
            value = var.image_upload_bucket_name
        }
        env {
            name  = "LOGGER_BUCKET"
            value = var.logger_bucket_name
        }
        ports {
          container_port = 8000
        }
        resources {
          limits = {
            "memory" = "1G"
            "cpu"    = "1"
          }
        }
      }
      container_concurrency = 1
      timeout_seconds       = 60
      service_account_name  = google_service_account.api_service_account.email
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }

  depends_on = [
    google_artifact_registry_repository_iam_member.docker_pusher_iam,
    google_service_account.api_service_account,
    docker_registry_image.api_image,
    google_sql_database_instance.image_manager_db
  ]
}

output "cloud_run_instance_url" {
  value = google_cloud_run_service.image_manager_app.status.0.url
}

output "cloud_run_instance_id" {
  value = google_cloud_run_service.image_manager_app.id
}

output "cloud_run_instance_service_name" {
  value = google_cloud_run_service.image_manager_app.name
}


# Create a policy that allows all users to invoke the API
data "google_iam_policy" "noauth" {
  provider = google-beta
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}


resource "google_cloud_run_service_iam_policy" "noauth" {
  provider    = google-beta
  location    = var.region
  project     = var.gc_project_id
  service     = google_cloud_run_service.image_manager_app.name
  policy_data = data.google_iam_policy.noauth.policy_data
}