#!/usr/bin/env python3

import iperf3

client = iperf3.Client()
client.duration = 1
client.server_hostname = '127.0.0.1'
client.port = 9631
client.protocol = 'tcp'


print('Connecting to {0}:{1}'.format(client.server_hostname, client.port))
result = client.run()

if result.error:
    print(result.error)
else:
    print(result)
