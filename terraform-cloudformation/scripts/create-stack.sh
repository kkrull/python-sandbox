#!/usr/bin/env bash

set -e

  # --parameters ParameterKey=KeyPairName,ParameterValue=TestKey \

aws cloudformation create-stack \
  --stack-name terraform-cloudformation \
  --template-body file://sns-template.json \
  $@
