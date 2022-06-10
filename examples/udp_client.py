#!/usr/bin/env python3

import iperf3

client = iperf3.Client()
client.duration = 1
client.server_hostname = "127.0.0.1"
client.port = 5201
client.protocol = "udp"


print(f"Connecting to {client.server_hostname}:{client.port}")
result = client.run()

if result.error:
    print(result.error)
else:
    print("")
    print("Test completed:")
    print(f"  started at         {result.time}")
    print(f"  bytes transmitted  {result.bytes}")
    print(f"  jitter (ms)        {result.jitter_ms}")
    print(f"  avg cpu load       {result.local_cpu_total}%\n")

    print("Average transmitted data in all sorts of networky formats:")
    print(f"  bits per second      (bps)   {result.bps}")
    print(f"  Kilobits per second  (kbps)  {result.kbps}")
    print(f"  Megabits per second  (Mbps)  {result.Mbps}")
    print(f"  KiloBytes per second (kB/s)  {result.kB_s}")
    print(f"  MegaBytes per second (MB/s)  {result.MB_s}")
