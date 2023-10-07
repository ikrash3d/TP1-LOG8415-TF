#!/bin/bash
pip install boto3 matplotlib

if [ $? -ne 0 ]; then
    echo "Dependency installation failed. Exiting."
    exit 1
fi

cd ../benchmark

source run.sh

python main.py
