#!/bin/bash

# exit when any command fails
set -e

# Goto current script folder
cd "$(dirname "$0")"

cd ..

rm -rf .venv
