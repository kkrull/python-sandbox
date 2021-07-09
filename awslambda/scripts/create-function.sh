#!/usr/bin/env bash

set -e

if (( $# != 1 ))
then
  echo "Usage: $0 <IAM Role ARN>"
  exit 1
fi

role_arn="$1"
shift

aws lambda create-function \
  --function-name=awscli-greeter \
  --handler=lambda_function.lambda_handler \
  --role="${role_arn}" \
  --runtime=python3.8 \
  --zip-file=fileb://awslambda.zip \
  | jq -r '.FunctionArn'
