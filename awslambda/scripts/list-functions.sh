#!/usr/bin/env bash

set -e

aws lambda list-functions | jq -r '.Functions[].FunctionName'
