#!/bin/bash

# Update the package index
sudo apt-get update

# Install required packages
sudo apt-get install -y ca-certificates curl

# Create the directory for Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings

# Download Docker's official GPG key
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc

# Set read permissions for the key
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add Docker's repository to Apt sources
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update the package index with Docker's repository
sudo apt-get update

echo "Docker repository added successfully."

sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin