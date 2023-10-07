#!/bin/bash
set -e # if ant commands fail, the script stops

echo -e "Creating instances...\n"

cd ../infrastructure

terraform.exe init

terraform.exe apply -auto-approve

# Retrieve the load balancer URL
load_balancer_url=$(terraform.exe output --raw load_balancer_url)

# Export the load_balancer_url variable
export load_balancer_url="$load_balancer_url"

echo -e "Everything was created successfully\n"
echo -e "-----------\n"

# Returning to root folder
cd ..