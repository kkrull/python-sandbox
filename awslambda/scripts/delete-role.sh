#!/usr/bin/env bash

set -e

aws iam detach-role-policy \
  --policy-arn=arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole \
  --role-name=awscli-greeter-role

aws iam delete-role --role-name=awscli-greeter-role
