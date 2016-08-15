iperf3 - Python interface to iperf3 using the libiperf API

Documentation on [readthedocs.org](https://iperf3.readthedocs.org)

[![Build Status](https://travis-ci.org/thiezn/iperf3-python.svg?branch=master)](https://travis-ci.org/thiezn/iperf3-python)
[![Coverage Status](https://coveralls.io/repos/github/thiezn/iperf3-python/badge.svg?branch=master)](https://coveralls.io/github/thiezn/iperf3-python?branch=master)

## Description

iperf3 for python provides a wrapper around the excellent iperf3 utility. iperf3 is a complete rewrite of the original iperf implementation. more information on the [official iperf3 site](https://iperf.fr/)

iperf3 introduced an API called libiperf that allows you to easily interact with iperf3 from other languages. This library provides a python wrapper around libiperf for easy integration into your own python scripts in a pythonic way

## Installation

Make sure iperf3 is present on your system. Installation on Ubuntu 14.04 LTS:

```
sudo apt-get install iperf3
```

NOTE: module not yet published on PyPi so pip install not available yet.
```
pip install iperf3
```

From github:
```
git clone https://github.com/thiezn/iperf3-python.git
cd iperf3-python
python3 setup.py install
```

### Server
```python
from iperf3 import IPerf3

server = IPerf3()
server.run()
```

### Client
```python
>>> from iperf3 import IPerf3
>>> client = IPerf3(role='c')
>>> client.duration = 1
>>> client.server_hostname = '127.0.0.1'
>>> client.server_port = 5201
>>> client.run()
{'intervals': [{'sum': {'omitted': False, 'bytes': 3905486848, 'start': 0, 'seconds': 1.00005, 'end': 1.00005, 'bits_per_second': 31242500000.0}, 'streams': [{'omitted': False, 'socket': 7, 'bytes': 3905486848, 'start': 0, 'seconds': 1.00005, 'end': 1.00005, 'bits_per_second': 31242500000.0}]}], 'start': {'system_info': 'Linux bxts488001.eu.rabonet.com 2.6.18-408.el5 #1 SMP Fri Dec 11 14:03:08 EST 2015 x86_64 x86_64 x86_64 GNU/Linux\n', 'timestamp': {'time': 'Mon, 15 Aug 2016 14:23:28 GMT', 'timesecs': 1471271008}, 'test_start': {'duration': 1, 'blksize': 131072, 'protocol': 'TCP', 'bytes': 0, 'blocks': 0, 'omit': 0, 'num_streams': 1, 'reverse': 0}, 'version': 'iperf 3.0.6', 'cookie': 'bxts488001.eu.rabonet.com.1471271008', 'connected': [{'local_host': '127.0.0.1', 'remote_host': '127.0.0.1', 'remote_port': 5201, 'socket': 7, 'local_port': 59464}], 'tcp_mss_default': 16384, 'connecting_to': {'host': '127.0.0.1', 'port': 5201}}, 'end': {'cpu_utilization_percent': {'remote_user': 0.0407711, 'host_user': 1.665, 'host_total': 96.216, 'remote_system': 1.83275, 'host_system': 94.4439, 'remote_total': 1.83507}, 'streams': [{'receiver': {'socket': 7, 'bytes': 3905486848, 'start': 0, 'seconds': 1.00005, 'end': 1.00005, 'bits_per_second': 31242500000.0}, 'sender': {'socket': 7, 'bytes': 3905486848, 'start': 0, 'seconds': 1.00005, 'end': 1.00005, 'bits_per_second': 31242500000.0}}], 'sum_sent': {'start': 0, 'seconds': 1.00005, 'end': 1.00005, 'bits_per_second': 31242500000.0, 'bytes': 3905486848}, 'sum_received': {'start': 0, 'seconds': 1.00005, 'end': 1.00005, 'bits_per_second': 31242500000.0, 'bytes': 3905486848}}}
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
