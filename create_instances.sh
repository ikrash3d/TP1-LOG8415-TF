set -e # if ant commands fail, the script stops

echo -e "Creating instances..."

terraform.exe init

terraform.exe apply -auto-approve

echo -e "\nEverything was created successfully"