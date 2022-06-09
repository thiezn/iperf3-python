#!/usr/bin/env python3


from iperf3 import Client


client = Client()
client.duration = 1
client.server_hostname = "127.0.0.1"
client.port = 5201

print(f"Connecting to {client.server_hostname}:{client.port}")
result = client.run_json()

if result is None:
    print("No result")
else:
    print(result)
