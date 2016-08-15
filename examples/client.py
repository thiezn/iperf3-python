#!/usr/bin/env python3

from iperf3 import IPerf3


def main():
    client = IPerf3(role='c')
    client.duration = 1
    client.server_hostname = '127.0.0.1'
    client.server_port = 5201
    client.run()


if __name__ == '__main__':
    main()
