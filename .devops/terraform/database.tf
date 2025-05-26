resource "google_sql_database_instance" "image_manager_db" {
  name             = "image-manager-api-db"
  database_version = "POSTGRES_16"

  deletion_protection = false

  settings {
    tier = "db-perf-optimized-N-2"
    deletion_protection_enabled = false
    disk_autoresize = false
    backup_configuration {
      enabled = false
    }
    data_cache_config {
      data_cache_enabled = false
    }

    ip_configuration {
      ipv4_enabled = true

      authorized_networks {
        name  = "allow-all"
        value = "0.0.0.0/0" # TODO: Restrict this to service account
      }
    }
  }
}

resource "google_sql_database" "default" {
  name     = var.db_instance_name
  instance = google_sql_database_instance.image_manager_db.name
}

resource "google_sql_user" "default" {
  name     = var.db_username
  instance = google_sql_database_instance.image_manager_db.name
  password_wo = var.db_password
}

