# FinOps AWS Infrastructure
# Provisions: Lambda scanner, EventBridge schedule, AWS Budgets, SNS, S3 report store

terraform {
  required_version = ">= 1.7"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.0" }
  }
  # Uncomment to use remote state
  # backend "s3" {
  #   bucket = "your-terraform-state"
  #   key    = "finops/terraform.tfstate"
  #   region = "us-east-1"
  # }
}

provider "aws" { region = var.region }

# ── S3 bucket — report storage ─────────────────────────────────────────────
resource "aws_s3_bucket" "reports" {
  bucket = "${var.project_name}-reports-${var.account_id}"
  tags   = local.tags
}

resource "aws_s3_bucket_versioning" "reports" {
  bucket = aws_s3_bucket.reports.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_lifecycle_configuration" "reports" {
  bucket = aws_s3_bucket.reports.id
  rule {
    id     = "expire-old-reports"
    status = "Enabled"
    expiration { days = 90 }
  }
}

# ── SNS topic — cost alerts ────────────────────────────────────────────────
resource "aws_sns_topic" "alerts" {
  name = "${var.project_name}-cost-alerts"
  tags = local.tags
}

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

# ── AWS Budgets — alert at 50/80/95/100% ──────────────────────────────────
resource "aws_budgets_budget" "monthly" {
  name         = "${var.project_name}-monthly"
  budget_type  = "COST"
  limit_amount = tostring(var.monthly_budget_usd)
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  dynamic "notification" {
    for_each = [50, 80, 95, 100]
    content {
      comparison_operator        = "GREATER_THAN"
      threshold                  = notification.value
      threshold_type             = "PERCENTAGE"
      notification_type          = "ACTUAL"
      subscriber_sns_topic_arns  = [aws_sns_topic.alerts.arn]
    }
  }
}

# ── IAM role for Lambda ────────────────────────────────────────────────────
resource "aws_iam_role" "lambda" {
  name = "${var.project_name}-lambda-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "lambda_policy" {
  name   = "finops-lambda-policy"
  role   = aws_iam_role.lambda.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["ce:GetCostAndUsage", "ec2:Describe*",
        "rds:DescribeDBInstances", "cloudwatch:GetMetricStatistics"],
        Resource = "*" },
      { Effect = "Allow", Action = ["s3:PutObject", "s3:GetObject"],
        Resource = "${aws_s3_bucket.reports.arn}/*" },
      { Effect = "Allow", Action = ["sns:Publish"],
        Resource = aws_sns_topic.alerts.arn },
      { Effect = "Allow",
        Action  = ["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"],
        Resource = "arn:aws:logs:*:*:*" },
    ]
  })
}

# ── Lambda — weekly cost scanner ───────────────────────────────────────────
resource "aws_lambda_function" "cost_scanner" {
  function_name = "${var.project_name}-cost-scanner"
  role          = aws_iam_role.lambda.arn
  handler       = "handler.handler"
  runtime       = "python3.11"
  timeout       = 300
  memory_size   = 512
  filename      = "${path.module}/../../lambda/cost_scanner.zip"

  environment {
    variables = {
      REPORTS_BUCKET = aws_s3_bucket.reports.bucket
      SNS_TOPIC_ARN  = aws_sns_topic.alerts.arn
    }
  }
  tags = local.tags
}

# ── EventBridge — every Monday 09:00 UTC ──────────────────────────────────
resource "aws_cloudwatch_event_rule" "weekly" {
  name                = "${var.project_name}-weekly-scan"
  description         = "Trigger FinOps cost scanner every Monday morning"
  schedule_expression = "cron(0 9 ? * MON *)"
  tags                = local.tags
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule      = aws_cloudwatch_event_rule.weekly.name
  target_id = "FinOpsWeeklyScan"
  arn       = aws_lambda_function.cost_scanner.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.cost_scanner.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.weekly.arn
}

locals {
  tags = {
    project    = var.project_name
    managed_by = "terraform"
    owner      = "ashwani.kumar"
  }
}
