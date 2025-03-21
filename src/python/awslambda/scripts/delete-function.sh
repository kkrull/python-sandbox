#!/usr/bin/env bash

set -e

aws lambda delete-function --function-name=awscli-greeter
