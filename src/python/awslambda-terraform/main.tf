terraform {
  backend "s3" {
    bucket = "kkrull-at-8thlight-python-sandbox"
    key    = "awslambda-terraform/main.tfstate"
    region = "us-east-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.27"
    }
  }

  required_version = ">= 0.14.9"
}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
}


## Topology

resource "aws_lambda_permission" "echo_trigger" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.echo.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.input_messages.arn
}

resource "aws_sns_topic_subscription" "input_messages_to_echo" {
  topic_arn = aws_sns_topic.input_messages.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.echo.arn
}


## SNS

output "workflow_01_input_messages_arn" {
  description = "ARN to the SNS topic that initiates the workflow"
  value       = aws_sns_topic.input_messages.arn
}

resource "aws_sns_topic" "input_messages" {
  name         = "awslambda-terraform-input-messages"
  display_name = "[awslambda-terraform 01] Input messages that initiate the workflow"
}


## Lambda

output "workflow_02_echo_arn" {
  description = "ARN to the Lambda function that processes events"
  value       = aws_lambda_function.echo.arn
}

# Build deployment artifact with scripts/build.sh
resource "aws_lambda_function" "echo" {
  description      = "[awslambda-terraform 02] Echos events received from SNS"
  filename         = "awslambda-terraform.zip"
  function_name    = "awslambda-terraform-echo"
  handler          = "tf_lambda_function.lambda_handler"
  role             = aws_iam_role.echo_role.arn
  runtime          = "python3.8"
  source_code_hash = filebase64sha256("awslambda-terraform.zip")
}

resource "aws_iam_role" "echo_role" {
  description         = "Assumed by awslambda-terraform-echo, when invoked"
  managed_policy_arns = [data.aws_iam_policy.AWSLambdaBasicExecutionRole.arn]
  name                = "awslambda-terraform-echo-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Sid = ""
      }
    ]
  })
}

data "aws_iam_policy" "AWSLambdaBasicExecutionRole" {
  name = "AWSLambdaBasicExecutionRole"
}
