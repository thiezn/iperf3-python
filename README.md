pyperf - Python interface to iperf3 using the iperf3 introduced API libiperf

url: https://readthedocs

[![Build Status](https://travis-ci.org/thiezn/iperf3-python.svg?branch=master)](https://travis-ci.org/thiezn/iperf3-python)
[![Coverage Status](https://coveralls.io/repos/github/thiezn/iperf3-python/badge.svg?branch=master)](https://coveralls.io/github/thiezn/iperf3-python?branch=master)

## Description

iperf3 for python provides a wrapper around the excellent iperf3 utility. iperf3 is a complete rewrite of the original iperf implementation. more information at [https://iperf.fr/]

iperf3 introduced an API called libiperf that allows you to easily interact with iperf3 from other languages. This library provides a python wrapper around libiperf for easy integration into your own python scripts in a pythonic way

## Quickstart

  pip install pyperf

### Server
```
server = PyPerf()
server.run()
```

### Client
```
client = PyPerf(role='c')
client.verbose = True
client.duration = 10
client.run()
```

## External Dependencies

iperf3
libiperf.0  (should come with iperf3)
Tested against Ubuntu 14.04 LTS standard iperf3 installation
