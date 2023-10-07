#!/bin/bash

# Access the env variables
source env_vars.sh

# Getting AWS credentials from the terminal
echo "Please provide your AWS Access Key: "
read AWS_ACCESS_KEY
echo

echo "Please provide your AWS Secret Access Key: "
read AWS_SECRET_ACCESS_KEY
echo

echo "Please provide your AWS Session Token Key: "
read AWS_SESSION_TOKEN
echo

# Exporting the credentials to be accessible in all the scripts
echo "export AWS_ACCESS_KEY='$AWS_ACCESS_KEY'" > env_vars.sh
echo "export AWS_SECRET_ACCESS_KEY='$AWS_SECRET_ACCESS_KEY'" >> env_vars.sh
echo "export AWS_SESSION_TOKEN='$AWS_SESSION_TOKEN'" >> env_vars.sh

echo -e "Starting Assignment 1...\n"
echo -e "-----------\n"

## Deploying the infrastructure
./create_instances.sh

## Sending the requests to the load balancer
docker pull ikrash3d/requests_app:latest

echo $load_balancer_url

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

# Killing the infrastructure
echo -e "Terminating infrastructure...\n"
./kill_instances.sh

# Clears the content of env_vars.sh
> env_vars.sh

echo -e "You successfully ended Assignment 1 :)"
