terraform {
  required_version = ">= 1.7"
  required_providers { aws = { source = "hashicorp/aws"; version = "~> 5.0" } }
}

provider "aws" { region = var.region }

resource "aws_s3_bucket" "reports" {
  bucket = "${var.project_name}-reports-${var.account_id}"
  tags   = local.tags
}

resource "aws_s3_bucket_lifecycle_configuration" "reports" {
  bucket = aws_s3_bucket.reports.id
  rule { id = "expire-90d"; status = "Enabled"; expiration { days = 90 } }
}

resource "aws_budgets_budget" "monthly" {
  name = "${var.project_name}-monthly"
  budget_type = "COST"; limit_amount = var.monthly_budget_usd; limit_unit = "USD"; time_unit = "MONTHLY"
  dynamic "notification" {
    for_each = [50, 80, 95, 100]
    content {
      comparison_operator       = "GREATER_THAN"; threshold = notification.value
      threshold_type            = "PERCENTAGE";   notification_type = "ACTUAL"
      subscriber_sns_topic_arns = [aws_sns_topic.alerts.arn]
    }
  }
}

resource "aws_sns_topic" "alerts" { name = "${var.project_name}-cost-alerts"; tags = local.tags }

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.alerts.arn; protocol = "email"; endpoint = var.alert_email
}

resource "aws_lambda_function" "cost_scanner" {
  function_name = "${var.project_name}-cost-scanner"
  role          = aws_iam_role.lambda.arn
  handler       = "handler.handler"; runtime = "python3.11"
  filename      = "${path.module}/../../lambda/cost_scanner.zip"
  timeout       = 300; memory_size = 512
  environment { variables = { REPORTS_BUCKET = aws_s3_bucket.reports.bucket; SNS_TOPIC_ARN = aws_sns_topic.alerts.arn } }
  tags = local.tags
}

resource "aws_cloudwatch_event_rule" "weekly" {
  name = "${var.project_name}-weekly"; schedule_expression = "cron(0 9 ? * MON *)"; tags = local.tags
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule = aws_cloudwatch_event_rule.weekly.name; target_id = "WeeklyFinOpsScan"; arn = aws_lambda_function.cost_scanner.arn
}

locals { tags = { project = var.project_name, managed_by = "terraform", owner = "ashwani.kumar" } }
