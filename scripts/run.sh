#!/bin/bash

## Getting AWS credentials from the terminal
export AWS_ACCESS_KEY="$1"
export AWS_SECRET_ACCESS_KEY="$2"
export AWS_SESSION_TOKEN="$3"

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
echo -e "Removing the docker container...\n"
docker rm requests_app_latest

# Run benchmark
echo -e "Running benchmarks...\n"
./run_benchmark.sh

## Killing the infrastructure
echo -e "Terminating infrastructure...\n"
./kill_instances.sh

echo -e "You successfully ended Assignment 1 :)"