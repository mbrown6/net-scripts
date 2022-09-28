#!/bin/bash

# Author: M Brown - matt.brown6@wework.com
# Date: 27 September 2022

# Simple Bash script to display one operational command
# Uses file ip_addr which is a list of host IP addresses

# Load host IPs into devices var
devices=$(cat ip_addr)

# Prompt for user name, -p switch prints prompt text
read -p  "Enter user name: " userName

# Prompt for password, -s switch does not echo input tp stdout stream
read -p "Enter password: " -s passWord

# Juniper operational command plus regex to filter output
read -p "Enter one valid junos operational/show command: " command1

#command1='show version | match "^Hostname:|^Model:|^Junos:"'

# Loop through devices var, use sshpass to store secret.
# SSH -o(options) No fingerprinting, timeout 4sec (optimize for unresponsive targets)
for device in ${devices}; do

    echo "Connecting to device: ${device}"
    sshpass -p$passWord ssh -o StrictHostKeyChecking=no -o ConnectTimeout=4 $userName@${device} ${command1}
    echo "====================================================================================================="

done
