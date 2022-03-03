# open_xconn.py connects to Opengear Terminal Servers and prints the device hostname
# Uses paramiko library to connect
# Uses getpass to prompt for a password, time to pause between commands
#
# Author: M. Browm
# Email: matt.brown6@wework.com

import paramiko
import time
from getpass import getpass
import csv

opengear_user = input('Opengear username: ')
passwd = getpass()

print('Opening hosts CSV file and extracting variables...')

with open('hosts.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        device = {
            'hostname': row[1],
            'username': opengear_user,
            'port': '22',
            'password': passwd,
        }

        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        print(f'Connecting to Opengear host {row[0]} with IP address {row[1]}')
        ssh_client.connect(**device, look_for_keys=False, allow_agent=False)

        shell = ssh_client.invoke_shell()
        shell.send('uname -n\n')
        time.sleep(1)

        output = shell.recv(1000)
        output = output.decode('utf-8')
        print(output)

        shell.send(f'config -s config.system.name={row[2]}\n')
        time.sleep(0.5)

        output = shell.recv(1000)
        output = output.decode('utf-8')
        print(output)

        shell.send('config -r systemsettings\n')
        time.sleep(2)

        output = shell.recv(1000)
        output = output.decode('utf-8')
        print(output)

        shell.send('uname -n\n')
        time.sleep(1)

        output = shell.recv(1000)
        output = output.decode('utf-8')
        print(output)

        if ssh_client.get_transport().is_active() == True:
            print(f'Closing connection to Opengear host {row[2]} with IP address {row[1]}...')
            ssh_client.close()



# Prompt user for OTS password
#passwd = getpass.getpass('Enter password: ')

# Create a device dictionary to connect to device
#device = {'hostname': '65.210.152.86',
#           'port': '22',
#           'username': 'svcconsole',
#           'password': passwd,
#           }

#print(f'Connecting to {device["hostname"]}')

#ssh_client.connect(**device, look_for_keys=False, allow_agent=False)
#
#shell = ssh_client.invoke_shell()
#shell.send('uname -n\n')
#time.sleep(0.5)
#
#output = shell.recv(10000)
#output = output.decode('utf-8')
#print(output)
#
#stdin, stdout, stderr = ssh_client.exec_command('config -s config.system.name=atl1-console\n')
#time.sleep(0.5)
#out = stdout.read()
#out = out.decode()
#print(out)
#
#print(stderr.read().decode())
#
#shell.send('config -r systemsettings\n')
#shell.send('uname -n\n')
#time.sleep(1)
#
#output2 = shell.recv(10000)
#output2 = output2.decode('utf-8')
#print(output2)
#
##print(ssh_client.get_transport().is_active())
#
## sending commands
#
#if ssh_client.get_transport().is_active() == True:
#    print('Closing connection')
#    ssh_client.close()
