variable "region"             { default = "us-east-1" }
variable "project_name"       { default = "finops-optimizer" }
variable "account_id"         { description = "AWS Account ID" }
variable "monthly_budget_usd" { default = 50000; type = number }
variable "alert_email"        { description = "Email for budget alerts" }
