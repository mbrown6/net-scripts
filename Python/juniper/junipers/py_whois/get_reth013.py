#!/usr/local/bin/python
#
# Name: get_reth013.py
#
# Connect to SRX cores and extract reth0/1/3 IP addresses
#
# Uses Netmiko with device_type: juniper_junos
#     Timeout, SSH, and AUthentication exceptions
#
# Reads "hosts.csv" to extract certain device connection values
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

        out1 = srx_open.send_command('show interfaces terse | match ^reth[013]\.0')

        print(out1)
        print(f'Disconnecting from Juniper {row[0]} with IP address {row[1]}')

        srx_open.disconnect()

        print('===========================================================================')
        print('\n')

#        with open('/Users/mbrown6/git_wework/net-scripts/Python/opengear/opengears/output/chg_name_results.txt', 'a') as results:
#            results.write(f'{out1} \n')
#            results.write(f'{out3} \n')
#            results.write(f'{out4} \n')
#            results.write(f'{out5} \n')
#            results.write('\n')
#            results.write('\n')
#            results.write('===========================================================================')
#            results.write('\n')
#            results.write('\n')
#
