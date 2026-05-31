# Azure FinOps Infrastructure
# Provisions: Azure Budget + Action Group + Logic App for Slack alerts

terraform {
  required_version = ">= 1.7"
  required_providers {
    azurerm = { source = "hashicorp/azurerm", version = "~> 3.0" }
  }
}

provider "azurerm" { features {} }

variable "subscription_id"   {}
variable "resource_group"     { default = "finops-rg" }
variable "monthly_budget_usd" { default = 20000 }
variable "alert_email"        {}

resource "azurerm_resource_group" "finops" {
  name     = var.resource_group
  location = "East US"
}

resource "azurerm_monitor_action_group" "finops" {
  name                = "finops-alerts"
  resource_group_name = azurerm_resource_group.finops.name
  short_name          = "finops"

  email_receiver {
    name          = "ops-email"
    email_address = var.alert_email
  }
}

resource "azurerm_consumption_budget_subscription" "monthly" {
  name            = "finops-monthly-budget"
  subscription_id = "/subscriptions/${var.subscription_id}"
  amount          = var.monthly_budget_usd
  time_grain      = "Monthly"

  time_period {
    start_date = "2025-01-01T00:00:00Z"
  }

  notification {
    enabled        = true
    threshold      = 80.0
    operator       = "GreaterThan"
    threshold_type = "Actual"
    contact_emails = [var.alert_email]
  }

  notification {
    enabled        = true
    threshold      = 100.0
    operator       = "GreaterThan"
    threshold_type = "Actual"
    contact_emails = [var.alert_email]
  }
}
