#!/usr/bin/env python3

from iperf3 import IPerf3

def main():
    server = IPerf3(role='s')
    server.run()


if __name__ == '__main__':
    main()
