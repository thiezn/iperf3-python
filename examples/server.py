#!/usr/bin/env python3

import iperf3

server = iperf3.Server()
print(f"Running server: {server.bind_address}:{server.port}")

while True:
    result = server.run()

    if result is not None:
        print(result)
