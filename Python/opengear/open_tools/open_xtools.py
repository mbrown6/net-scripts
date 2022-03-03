import paramiko
import time

def connect(device_name, ip_addr, ssh_port, user, passwd):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f'Connecting to host: {device_name} IP address: {ip_addr}')
    ssh_client.connect(hostname=ip_addr, port=ssh_port, username=user, password=passwd,
                       look_for_keys=False, allow_agent=False)
    return ssh_client

def get_shell(ssh_client):
    shell = ssh_client.invoke_shell()
    return shell

def send_command(shell, command, timeout=1):
    print(f'Sending command: {command}')
    shell.send(command + '\n')
    time.sleep(timeout)

def show(shell, n=10000):
    output = shell.recv(n)
    return output.decode()

def close(ssh_client):
    if ssh_client.get_transport().is_active() == True:
        print('Closing connection...')
        ssh_client.close()

client = connect('atl1-console', '65.210.152.86', '22', 'svcconsole', '5wdD0;YhAX}4rB8yPy' )
shell = get_shell(client)

send_command(shell, 'uname -n')

output = show(shell)
print(output)


