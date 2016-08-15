iperf3 - Python interface to iperf3 using the libiperf API

Documentation on [readthedocs.org](https://iperf3.readthedocs.org)

[![Build Status](https://travis-ci.org/thiezn/iperf3-python.svg?branch=master)](https://travis-ci.org/thiezn/iperf3-python)
[![Coverage Status](https://coveralls.io/repos/github/thiezn/iperf3-python/badge.svg?branch=master)](https://coveralls.io/github/thiezn/iperf3-python?branch=master)

## Description

iperf3 for python provides a wrapper around the excellent iperf3 utility. iperf3 is a complete rewrite of the original iperf implementation. more information on the [official iperf3 site](https://iperf.fr/)

iperf3 introduced an API called libiperf that allows you to easily interact with iperf3 from other languages. This library provides a python wrapper around libiperf for easy integration into your own python scripts in a pythonic way

## Quickstart

```
pip install iperf3
```

### Server
```python
from iperf3 import IPerf3
server = IPerf3()
server.run()
```

### Client
```python
from iperf3 import IPerf3
client = IPerf3(role='c')
client.verbose = True
client.duration = 10
client.run()
```

## External Dependencies

- iperf3
- libiperf.0  (should come with iperf3)

## Testing
Tested against Ubuntu 14.04 LTS standard iperf3 installation

Tested against Python versions:
- 2.7
- 3.3
- 3.4
- 3.5
- 3.5-dev
- nightly
