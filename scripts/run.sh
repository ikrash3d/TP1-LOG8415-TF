#!/bin/bash

## Getting AWS credentials from the terminal
# export aws_access_key_id="$1"
# export aws_secret_access_key="$2"
# export aws_session_token="$3"

echo -e "Starting Assignment 1...\n"
echo -e "-----------\n"

## Deploying the infrastructure
./create_instances.sh

source ./create_instances.sh

## Sending the requests to the load balancer
docker pull ikrash3d/requests_app:latest

docker run -e load_balancer_url="$load_balancer_url" -d --name requests_app_latest ikrash3d/requests_app:latest
echo -e "\nSending requests...\n"

## Shows the prints of the requests_app
docker logs -f requests_app_latest

# Removing the docker container
echo e "Removing the docker container\n"
docker rm requests_app_latest

## TODO : Run the benchmark

## Killing the infrastructure
#./kill_instances.sh

echo -e "You successfully ended Assignment 1 :)"