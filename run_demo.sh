#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo $'Give name of module to be executed as parameter:\n$ run_demo.sh <python_module_name>\n'
    echo $'For example: ./run_demo.sh bouncing_ball'
    exit 0
fi

poetry run python -m src.$1
