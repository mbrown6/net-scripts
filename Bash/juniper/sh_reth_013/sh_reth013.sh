#!/bin/bash

# Author: M Brown - matt.brown6@wework.com
# Date: 25 November 2021

# Simple Bash script to extract reth0/1/3.0 IP addresses from Juniper SRX core firewalls
# Uses "hosts" textfile which is a list of SRX host IP addresses

# This script is dependent on SSHPASS to store user and passwd information. Make sure
# SSHPASS is installed on the local machine before executing this script

# Load host IPs into devices var
devices=$(cat hosts)

# Prompt for user name, -p switch prints prompt text
read -p  "Enter username: " userName

# Prompt for password, -s switch does not echo input to stdout stream
read -p "Enter password: " -s passWord

# Juniper operational command +regex to filter output to reth0, reth1, and reth3 ints
command1="show interfaces terse | match ^reth[013]\.0"

# Loop through devices var, use sshpass to store secret.
# SSH -o(options) No fingerprinting, timeout 4sec (optimize for unresponsive targets)
for device in ${devices}; do

    echo "Connecting to device: ${device}"
    sshpass -p$passWord ssh -o StrictHostKeyChecking=no -o ConnectTimeout=4 $userName@${device} ${command1}
    echo "============================================================="
    printf "\n"

done
