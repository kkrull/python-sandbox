#!/usr/bin/env bash

set -e

aws lambda invoke \
  response.json \
  --cli-binary-format=raw-in-base64-out \
  --function-name=awscli-greeter \
  --log-type=Tail

cat response.json
