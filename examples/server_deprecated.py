#!/usr/bin/env python3

import iperf3


server = iperf3.Server()
print(f"Running server: {server.bind_address}:{server.port}")

while True:
    result = server.run_deprecated()

    if result.error:
        print(result.error)
    else:
        print("")
        print(f"Test results from {result.remote_host}:{result.remote_port}")
        print(f"  started at         {result.time}")
        print(f"  bytes received     {result.received_bytes}")

        print("Average transmitted received in all sorts of networky formats:")
        print(f"  bits per second      (bps)   {result.received_bps}")
        print(f"  Kilobits per second  (kbps)  {result.received_kbps}")
        print(f"  Megabits per second  (Mbps)  {result.received_Mbps}")
        print(f"  KiloBytes per second (kB/s)  {result.received_kB_s}")
        print(f"  MegaBytes per second (MB/s)  {result.received_MB_s}")
        print("")
