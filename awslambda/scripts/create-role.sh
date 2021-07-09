#!/usr/bin/env bash

set -e

role_arn=$(aws iam create-role \
  --role-name=awscli-greeter-role \
  --assume-role-policy-document='{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}' \
  | jq -r '.Role.Arn')

aws iam attach-role-policy \
  --policy-arn=arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole \
  --role-name=awscli-greeter-role

echo $role_arn
