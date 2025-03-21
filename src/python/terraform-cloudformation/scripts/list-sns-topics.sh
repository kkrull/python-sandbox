#!/usr/bin/env bash

set -e

aws sns list-topics $@
