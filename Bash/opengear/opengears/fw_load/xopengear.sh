#!/bin/bash
#
# xopengear.sh loads FW rules onto one OTS device
#
# Prompts for Opengear host IP, user, password
#
# Ping Opengear IP:
#    if Opengear is reachable, load base FW configuration
#    else echo IP address unreachable
#
# Run FW config, run Opengear configurator
#
# Date: 12-06-2021
# Author: M Brown
# Email: matt.brown6@wework.com
#
#
# Prompt for Opengear IP address
read -p "Enter Opengear IP address: " ip_addr

# Prompt for user name, -p switch prints prompt text
read -p  "Enter user name: " user

# Prompt for password, -s switch does not echo input tp stdout stream
read -p "Enter password: " -s pass

# Global variables
command1="./fw_rules.sh"
command2="config -g config.firewall | wc -l"
command3="rm fw_rules.sh"

# Ping device to test reachability, return result to stdout
ping -c 1 ${ip_addr} >/dev/null

if [ $? -eq 0 ]
then
    echo "Opengear IP ${ip_addr} is reachable."
    sshpass -p$pass scp -o StrictHostKeyChecking=no -o ConnectTimeout=4 fw_rules.sh ${user}@${ip_addr}:/etc/config/users/svcconsole
    sleep 3
    echo "Opengear IP ${ip_addr} FW rules are loaded "
    sshpass -p$pass ssh -o StrictHostKeyChecking=no -o ConnectTimeout=4 $user@${p_addr} ${command1}
    sleep 300
    sshpass -p$pass ssh -o StrictHostKeyChecking=no -o ConnectTimeout=4 $user@${p_addr} ${command2}
    sleep 3
    sshpass -p$pass ssh -o StrictHostKeyChecking=no -o ConnectTimeout=4 $user@${p_addr} ${command3}
elif [ $? -ne 0 ]
then
    echo "Opengear IP ${ip_addr} is not reachable."
fi
