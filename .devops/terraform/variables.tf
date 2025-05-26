variable "gc_project_id" {}
variable "region" {}
variable "zone" {}


variable "repository" {
  description = "Artifact Registry repository's name"
  type        = string
  default     = "docker-repository"
}
variable "docker_image" {
  description = "The name of the Docker image"
  type        = string
  default     = "image-manager-api"
}

variable "db_instance_name" {
  sensitive = true
}
variable "db_username" {
  sensitive = true
}
variable "db_password" {
  sensitive = true
}

variable "image_upload_bucket_name" {}
variable "logger_bucket_name" {}
