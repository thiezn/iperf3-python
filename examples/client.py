#!/usr/bin/env python3

import iperf3

def main():
    client = iperf3.Client()
    client.duration = 1
    client.server_hostname = '127.0.0.1'
    client.server_port = 5201
    response = client.run()
    print(response)


if __name__ == '__main__':
    main()
