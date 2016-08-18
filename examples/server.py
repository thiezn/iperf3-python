#!/usr/bin/env python3

import iperf3


def main():
    server = iperf3.Server()
    print('Running server: {0}:{1}'.format(server.bind_address, server.port))
    results = server.run()
    print(results)


if __name__ == '__main__':
    main()
