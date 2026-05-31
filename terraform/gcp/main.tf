# GCP FinOps Infrastructure
# Provisions: GCP Budget alert + Pub/Sub + Cloud Function

terraform {
  required_version = ">= 1.7"
  required_providers {
    google = { source = "hashicorp/google", version = "~> 5.0" }
  }
}

variable "project_id"        {}
variable "billing_account"   {}
variable "monthly_budget_usd" { default = 10000 }
variable "alert_email"        {}

provider "google" { project = var.project_id }

resource "google_pubsub_topic" "budget_alerts" {
  name = "finops-budget-alerts"
}

resource "google_billing_budget" "monthly" {
  billing_account = var.billing_account
  display_name    = "FinOps Monthly Budget"

  budget_filter {
    projects = ["projects/${var.project_id}"]
  }

  amount {
    specified_amount {
      currency_code = "USD"
      units         = tostring(var.monthly_budget_usd)
    }
  }

  threshold_rules { threshold_percent = 0.5 }
  threshold_rules { threshold_percent = 0.8 }
  threshold_rules { threshold_percent = 1.0 }

  all_updates_rule {
    pubsub_topic = google_pubsub_topic.budget_alerts.id
  }
}
