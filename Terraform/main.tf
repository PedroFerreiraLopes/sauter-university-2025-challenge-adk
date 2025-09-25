terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}


provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
  zone    = var.gcp_zone
  credentials = file("credentials.json")
}

resource "google_project_service" "compute_api" {
  project = var.gcp_project_id
  service = "compute.googleapis.com"
}


resource "google_compute_network" "vpc_network" {
  name                    = "${var.gcp_project_id}-vpc" 
  auto_create_subnetworks = true
}


resource "google_compute_instance" "vm_instance" {
  name         = "projeto-sauter-vm"
  machine_type = "e2-micro"
  zone         = var.gcp_zone

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  
  network_interface {
    network = google_compute_network.vpc_network.id
    access_config {
     }
  }

  
  depends_on = [
    google_compute_network.vpc_network
  ]

}

module "notification_channel" {
  source              = "./modules/notification_channel"
  notification_emails = var.notification_emails
}

module "billing_budget" {
  source                   = "./modules/billing_budget"
  billing_account_id       = var.billing_account_id
  project_id               = var.gcp_project_id
  budget_amount            = var.budget_amount_usd
  notification_channel_ids = module.notification_channel.channel_ids
}
