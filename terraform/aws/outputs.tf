output "reports_bucket"      { value = aws_s3_bucket.reports.bucket }
output "sns_topic_arn"       { value = aws_sns_topic.alerts.arn }
output "lambda_function_name"{ value = aws_lambda_function.cost_scanner.function_name }
output "budget_name"         { value = aws_budgets_budget.monthly.name }
