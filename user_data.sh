#!/bin/bash
# Install necessary dependencies
sudo yum update -y
sudo yum install -y python3
sudo yum install -y python3-pip
sudo yum install -y git

# Clone your Flask app repository
git clone https://github.com/ikrash3d/TP1-LOG8415-TF.git

# Install app dependencies
cd TP1-LOG8415-TF/flask_app
sudo pip3 install -r requirements.txt

# Start the Flask app
sudo python3 flask_app.py

