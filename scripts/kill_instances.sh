#!/bin/bash
set -e # if any commands fail, the script stops

echo -e "Destroying all instances...\n"

cd ../infrastructure

terraform.exe destroy -auto-approve

echo -e "Everything was deleted successfully\n"
echo -e "-----------\n"
