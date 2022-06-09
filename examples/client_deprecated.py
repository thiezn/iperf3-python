#!/usr/bin/env python3

from iperf3 import iperf3

client = iperf3.Client()
client.duration = 1
client.server_hostname = "127.0.0.1"
client.port = 5201

print(f"Connecting to {client.server_hostname}:{client.port}")
result = client.run_deprecated()

if result.error:
    print(result.error)
else:
    print("")
    print("Test completed:")
    print(f"  started at         {result.time}")
    print(f"  bytes transmitted  {result.sent_bytes}")
    print(f"  retransmits        {result.retransmits}")
    print(f"  avg cpu load       {result.local_cpu_total}%\n")

    print("Average transmitted data in all sorts of networky formats:")
    print(f"  bits per second      (bps)   {result.sent_bps}")
    print(f"  Kilobits per second  (kbps)  {result.sent_kbps}")
    print(f"  Megabits per second  (Mbps)  {result.sent_Mbps}")
    print(f"  KiloBytes per second (kB/s)  {result.sent_kB_s}")
    print(f"  MegaBytes per second (MB/s)  {result.sent_MB_s}")
