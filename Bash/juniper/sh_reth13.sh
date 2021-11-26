#!/bin/bash

# Author: M Brown - matt.brown6@wework.com
# Date: 25 November 2021

# Simple Bash script to extract reth1/3.0 IP addresses from Juniper SRX core firewalls
# Uses textfile test1.txt which is a list of host IP addresses

# Load host IPs into devices var
devices=$(cat test1.txt)

# Prompt for user name, -p switch prints prompt text
read -p  "Enter user name: " userName

# Prompt for password, -s switch does not echo input tp stdout stream
read -p "Enter password: " -s passWord

# Juniper operational command plus regex to filter output
commands="show interfaces terse | match ^reth[13]\.0"

# Loop through devices var, use sshpass to store secret.
# SSH -o(options) No fingerprinting, timeout 4sec (optimize for unresponsive targets)
for device in ${devices}; do

    echo "Connecting to device: ${device}"
    sshpass -p$passWord ssh -o StrictHostKeyChecking=no -o ConnectTimeout=4 $userName@${device} ${commands}
    echo "============================================================="

done
