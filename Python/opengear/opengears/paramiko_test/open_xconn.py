# open_xconn.py connects to Opengear Terminal Servers and prints the device hostname
# Uses paramiko library to connect
# Uses getpass to prompt for a password, time to pause between commands
#
# Author: M. Browm
# Email: matt.brown6@wework.com

import paramiko
import time
import getpass

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Prompt user for OTS password
passwd = getpass.getpass('Enter password: ')

# Create a device dictionary to connect to device
device = {'hostname': '65.210.152.86',
           'port': '22',
           'username': 'svcconsole',
           'password': passwd,
           }

print(f'Connecting to {device["hostname"]}')

ssh_client.connect(**device, look_for_keys=False, allow_agent=False)

shell = ssh_client.invoke_shell()
shell.send('uname -n\n')
time.sleep(0.5)

output = shell.recv(10000)
output = output.decode('utf-8')
print(output)

stdin, stdout, stderr = ssh_client.exec_command('config -s config.system.name=atl1-console\n')
time.sleep(0.5)
out = stdout.read()
out = out.decode()
print(out)

print(stderr.read().decode())

shell.send('config -r systemsettings\n')
shell.send('uname -n\n')
time.sleep(1)

output2 = shell.recv(10000)
output2 = output2.decode('utf-8')
print(output2)

#print(ssh_client.get_transport().is_active())

# sending commands

if ssh_client.get_transport().is_active() == True:
    print('Closing connection')
    ssh_client.close()
