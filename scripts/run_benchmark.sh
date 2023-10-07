#!/bin/bash
pip install boto3 matplotlib

cd ../benchmark

source ./run.sh

python main.py