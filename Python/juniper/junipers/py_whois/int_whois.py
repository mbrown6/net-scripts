#!/usr/local/bin/python
#
# Name: int_whois.py
#
# Connect to SRX cores and extract reth0/1/3 IP addresses
#
# Uses Netmiko with device_type: juniper_junos
#     Timeout, SSH, and AUthentication exceptions
#
# Reads "hosts.csv" to extract certain device connection values
#
# Gets IP and runs them against whois
#
# Date: 12-6-2021
# Author: M. Brown
# Email: matt.brown6@wework.com

from netmiko import Netmiko
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException
from getpass import getpass
import csv
import whois

srx_user = input('Enter username: ')
passwd = getpass()

with open('/Users/mbrown6/git_wework/net-scripts/Python/juniper/junipers/py_whois/hosts.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        device = {
            'host': row[1],
            'username': srx_user,
            'password': passwd,
            'device_type': row[3],
        }

        print(f'Connecting to Juniper {row[0]} with IP address {row[1]}')

        try:
            srx_open = Netmiko(**device)
        except (AuthenticationException):
            print(f'Authentication failure to Opengear {row[0]} with IP address {row[1]}')
            continue
        except (NetMikoTimeoutException):
            print(f'Connection timeout to Opengear {row[0]} with IP address {row[1]}')
            continue
        except (EOFError):
            print(f'EOF while connecting to Opengear {row[0]} with IP address {row[1]}')
            continue
        except (SSHException):
            print(f'SSH issue while connecting to {row[0]} with IP address {row[1]}')
            continue
        except Exception as unknown_error:
            print(f'Some other error: {unknown_error}')
            continue

        out = srx_open.send_command('show interfaces terse | match ^reth[013]\.0')

        print(out)

        wan_interface = dict()
        show_interfaces_lines = out.splitlines()
        for line in show_interfaces_lines:
            values = line.split()

            print(f'{values[0]}: {values[4].split("/")}')

        srx_open.disconnect()


