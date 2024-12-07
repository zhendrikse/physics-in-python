#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo $'Give name of module to be executed as parameter:\n\n$ run_demo.sh <python_module_name>'
    exit 0
fi

PYTHONPATH=.. poetry run python -m $1
