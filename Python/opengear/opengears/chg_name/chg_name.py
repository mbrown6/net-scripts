# chg_name.py connects to Opengear Terminal Servers and changes the hostname
#
# Uses Netmiko with device_type: linux
#     Timeout, SSH, and AUthentication exceptions
#
# Reads "hosts.csv" to extract certain device connection values
#
# Date: 12-3-2021
# Author: M. Brown
# Email: matt.brown6@wework.com

from netmiko import Netmiko
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import SSHException
from getpass import getpass
import csv

opengear_user = input('Opengear username: ')
passwd = getpass()

print('\n')
print('Opening hosts CSV file and extracting variables...')
print('===========================================================================')

with open('/Users/mbrown6/git_wework/net-scripts/Python/opengear/opengears/hosts/usc/hosts.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        device = {
            'host': row[1],
            'username': opengear_user,
            'password': passwd,
            'device_type': row[3],
        }

        print(f'Connecting to Opengear {row[0]} with IP address {row[1]}')

        try:
            x_open = Netmiko(**device)
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

        out1 = x_open.send_command('uname -n')
        out2 = x_open.send_command(f'config -s config.system.name={row[4]}')
        out3 = x_open.send_command(f'config -g config.system.name')
        out4 = x_open.send_command(f'config -r systemsettings')
        out5 = x_open.send_command('uname -n')

        print(out1)
        print(out3)
        print(out4)
        print(out5)
        print(f'Disconnecting from Opengear {row[4]} with IP address {row[1]}')

        x_open.disconnect()

        print('\n')
        print('===========================================================================')
        print('\n')

        with open('/Users/mbrown6/git_wework/net-scripts/Python/opengear/opengears/output/chg_name_results.txt', 'a') as results:
            results.write(f'{out1} \n')
            results.write(f'{out3} \n')
            results.write(f'{out4} \n')
            results.write(f'{out5} \n')
            results.write('\n')
            results.write('\n')
            results.write('===========================================================================')
            results.write('\n')
            results.write('\n')

