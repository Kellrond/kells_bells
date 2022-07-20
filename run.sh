#!/usr/bin/env bash
PWD=$(pwd)
set -e
source $PWD/venv/bin/activate

python3 $PWD/main.py

deactivate