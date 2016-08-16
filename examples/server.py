#!/usr/bin/env python3

import iperf3


def main():
    server = iperf3.Server()
    results = server.run()
    print(results)


if __name__ == '__main__':
    main()
