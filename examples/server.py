#!/usr/bin/env python3


from iperf3.iperf3 import Server


server = Server()
print(f"Running server: {server.bind_address}:{server.port}")

while True:
    result = server.run_json()

    if result is None:
        print("No result")

    else:
        print(result)
