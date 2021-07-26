#!/usr/bin/env bash

set -e

aws cloudformation describe-stack-resources \
  --stack-name terraform-cloudformation \
  $@
