with open ('hosts.txt', 'r') as hostfile:
    data = hostfile.readlines()

for line in data:
    values = line.split(',')
    name = values[0]
    ip_addr = values[1]
    new_name = values[2]

    print(f'The device name is {name}')
    print(f'The device IP address is {ip_addr}')
    print(f'The device new name is {new_name}')
