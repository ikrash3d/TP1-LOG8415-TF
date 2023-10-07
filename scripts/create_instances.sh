#!/bin/bash
set -e # if any commands fail, the script stops

echo -e "Creating instances...\n"

cd ../infrastructure

source ../run.sh

terraform.exe init

terraform.exe apply -auto-approve -var="aws_access_key_id=AWS_ACCESS_KEY" -var="aws_secret_access_key=AWS_SECRET_ACCESS_KEY" -var="aws_session_token=AWS_SESSION_TOKEN"

# Retrieve the load balancer URL
load_balancer_url=$(terraform.exe output --raw load_balancer_url)

# Export the load_balancer_url variable
export load_balancer_url="$load_balancer_url"

echo -e "Everything was created successfully\n"
echo -e "-----------\n"

# Returning to root folder
cd ..
