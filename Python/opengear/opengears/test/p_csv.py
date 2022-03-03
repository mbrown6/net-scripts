import csv

with open('/Users/mbrown6/git_wework/net-scripts/Python/opengear/opengears/hosts.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        print(f'Connecting to Opengear host {row[0]} with IP address {row[1]}...')
        print(f'Updating Opengear hostname to {row[2]}')


