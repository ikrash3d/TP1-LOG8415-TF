#!/bin/bash

# Access the env variables
source env_vars.sh

# Install the necessary dependencies
pip install boto3 matplotlib

# Looks if the dependencies are correctly installed
if [ $? -ne 0 ]; then
    echo "Dependency installation failed. Exiting."
    exit 1
fi

cd ../benchmark

# Run the benchmark script
python3 main.py
