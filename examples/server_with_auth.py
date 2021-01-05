#!/usr/bin/env python3

import iperf3.iperf3
import re

server = iperf3.Server()
rsa_privkey = '''MIIEpAIBAAKCAQEA0AKoqwFjngchlz/If0DLBP+5/dmgWpJKgVlHokkQk3ZRj0PR
bSt8zLnmbytsZL8QdknhRuNZXT3S0kY/E5V6+jbTaM59MjIfr0n76xIwIC9fxp6P
qb0YNvC3T2seX8x9GQZsm8k8Ur7hQtLpi3DTibGgD7I4qfquqg37b+4ZHRnwlok2
0tznkoboCGqpzp2DsgXfpstEAA8lajkEdkJopx6VDq8r3o8Gu33TTyAzSZn0ATcN
jGe7jJ/RiGGJb3X2qnGsqRgECoTmXG1M/H1G5cXp/TLQKOx1pnQe9BNrIaMZdiNo
+FBU2XYqqMRA4w+Blu14hURTm4APL316P5gtzwIDAQABAoIBAQCklNX7p/e3+5B6
ab8r4IpCBEyXK/ASeZl1yrxBDWqOIpnZryEvLa9rFNPcthDnjb1qun4CZrQ4cEg0
k9wolKde/q47SNYKN1qWiQVIM3XcoV84ehDVjoZwQfnoXqsDxXpdqJWalZijJ+B3
zQV4jObzFZW9lZf79hro9nMxVsSMHqLohg08trPd8OMY+zIpXGa1+8XgowXXWLfW
h8tFUv8kqD6S61oBN0d41SntVKB5s+shweY+rHy8PtazyQS7MPnAkcVQUMNlMyzH
57/f1/6hOF7xJJrUf6XhIdrTioVmmTvsmGFI88BlPTzcSNRJH+IDbOd+3yA/Yc+a
6ny37woxAoGBAOm5gt1FZ5DPkGZdmiNufSc6Qz9MThBX4DckQhEYQkn6IQIeBhYN
bn1W6E8q0x9TWFOiW2QcrzUrnS4JJvf5Lo8GkP9ECzg3XaNeTX3N+jE3QsFGskYz
t54YeqQvq9N0h20qBV5Msm0aQT4HiNsuvdR4R2DdsaUG845RXCk3xKK1AoGBAOPV
w0SToTw8tsZ/qgz2q65mO1NJLPvqx6Tne7xLiPWmyGq1SgtquolBDgDbNkAi0zj2
iROlmVON8svZM2/NCsjSMsd4oScRylk+OQxLCc+4Imn7S68ltFx7lK/uXzHuJOmT
UP3RYRhj/mFrnk+bW2gBiTyDzoWhe7uQdjbDlEzzAoGAM8WhBEycbUpdDR/Mxe5y
kJ7qSHopjJs6klxYuhqqjGJ4r1RhOr9M6zy2BttQms7GcPg00E8+TEPV9F2YoTM0
KgBlW/YBmjlBZ6+68JQQyJgaFGAJm11XXhDEEdxxbkyQtxCo0cOhfmNjck8O9KY8
7HScMwvIjuqkRrEk/ghZaUUCgYAdSfitUzEyFjgE8pqAyiEt7VSJE2omBHuf1mZQ
wYEc21D+bsnTB+htBqDvOT8TJabztrXOgcZhOGlTDVwQblKJmIQQopBM/nt914Lr
8qWTP3+lEjobjQRPs09dAo7YU14JbPfHeWg7A3fLPFOAtl8c0r26utMM2MKYTSz1
Q1VIQwKBgQC2bHZ/97JyeFCdprerX5khUv7tgZimaTlApVbx+GiF4ifpUcy1+aNe
ECtT7nEtplN1P1AinWUEXCtjETzR5eEKv0Rxof/YUXVMBr5XwpQZujNtmPHEgnNM
QnYrdXI6zUXOntc0SfDNkVJI9wLIM2flZ1/oV3mboTk/a3hefbY6zQ=='''
server.rsa_privkey = re.sub(r"[\n\t\s]*", "", rsa_privkey)
server.authorized_users = "authorized_users.txt"
print('Running server: {0}:{1}'.format(server.bind_address, server.port))

while True:
    result = server.run()

    if result.error:
        print(result.error)
    else:
        print('')
        print('Test results from {0}:{1}'.format(result.remote_host,
                                                 result.remote_port))
        print('  started at         {0}'.format(result.time))
        print('  bytes received     {0}'.format(result.received_bytes))

        print('Average transmitted received in all sorts of networky formats:')
        print('  bits per second      (bps)   {0}'.format(result.received_bps))
        print('  Kilobits per second  (kbps)  {0}'.format(result.received_kbps))
        print('  Megabits per second  (Mbps)  {0}'.format(result.received_Mbps))
        print('  KiloBytes per second (kB/s)  {0}'.format(result.received_kB_s))
        print('  MegaBytes per second (MB/s)  {0}'.format(result.received_MB_s))
        print('')
