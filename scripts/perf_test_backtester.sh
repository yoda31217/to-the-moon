#!/bin/bash

# exit when any command fails
set -e

# Goto current script folder
cd "$(dirname "$0")"

cd ..

python3 ./perf_tests/backtester/perf_test_backtester.py
