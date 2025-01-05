#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo $'Give name of module to be executed as parameter:\n$ run_demo.sh <python_module_name>\n'
    echo $'For example: ./run_glowscript.sh bouncing_ball'
    exit 0
fi

poetry run python -m src.glowscript.$1
