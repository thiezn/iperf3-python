iperf3-python: Python wrapper around iperf3
===========================================

|Build Status| |Coverage Status| |Documentation Status|

Detailed documentation at
`iperf3-python.readthedocs.org <https://iperf3-python.readthedocs.org/>`__

iperf3 for python provides a wrapper around the excellent iperf3
utility. iperf3 is a complete rewrite of the original iperf
implementation. more information on the `official iperf3
site <http://software.es.net/iperf/>`__

iperf3 introduced an API called libiperf that allows you to easily
interact with iperf3 from other languages. This library provides a
python wrapper around libiperf for easy integration into your own python
scripts in a pythonic way

Installation
------------

First you have to make sure the iperf3 utility is present on your system as the
python module wraps around the libiperf API provided by it. 

The common linux distributions offer installations from their own repositories. These
might be out of date so installation from the official `iperf3 website <http://software.es.net/iperf/>`__
is preferred.

Otherwise try your OS package manager:

- Ubuntu 14.04 LTS:

.. code:: bash

    sudo apt-get install iperf3

- CenOS/RedHat

.. code:: bash

    sudo yum install iperf3

Once the iperf3 utility is installed the simplest way to install the python wrapper is through
`PyPi <https://pypi.python.org/pypi/iperf3>`__

.. code:: bash

    pip install iperf3

You can also install directly from the github repository:

.. code:: bash

    git clone https://github.com/thiezn/iperf3-python.git
    cd iperf3-python
    python3 setup.py install

Quickstart
----------

For detailed examples check out the `examples page <http://iperf3-python.readthedocs.io/en/latest/examples.html>`__

**Server**

.. code:: python

    >>> import iperf3

    >>> server = iperf3.Server()
    >>> server.run()
    {'start': {'accepted_connection': {'host': '127.0.0.1', 'port': 45995}, 'version': 'iperf 3.0.6', 'timestamp': {'timesecs': 1471333681, 'time': 'Tue, 16 Aug 2016 07:48:01 GMT'}, 'connected': [{'local_host': '127.0.0.1', 'local_port': 5201, 'socket': 8, 'remote_port': 45996, 'remote_host': '127.0.0.1'}], 'tcp_mss_default': 16384, 'system_info': 'Linux server.local 2.6.18-408.el5 #1 SMP Fri Dec 11 14:03:08 EST 2015 x86_64 x86_64 x86_64 GNU/Linux\n', 'test_start': {'num_streams': 1, 'blksize': 131072, 'omit': 0, 'protocol': 'TCP', 'bytes': 0, 'blocks': 0, 'duration': 1, 'reverse': 0}, 'cookie': 'server.local.1471333681'}, 'intervals': [{'streams': [{'bits_per_second': 18954200000.0, 'socket': 8, 'end': 1.00009, 'omitted': False, 'bytes': 2369470464, 'start': 0, 'seconds': 1.00009}], 'sum': {'omitted': False, 'bits_per_second': 18954200000.0, 'end': 1.00009, 'bytes': 2369470464, 'start': 0, 'seconds': 1.00009}}, {'streams': [{'bits_per_second': 19773800000.0, 'socket': 8, 'end': 1.0388, 'omitted': False, 'bytes': 95682560, 'start': 1.00009, 'seconds': 0.0387108}], 'sum': {'omitted': False, 'bits_per_second': 19773800000.0, 'end': 1.0388, 'bytes': 95682560, 'start': 1.00009, 'seconds': 0.0387108}}], 'end': {'cpu_utilization_percent': {'remote_user': 1.75867, 'remote_system': 63.1275, 'host_user': 0.0386741, 'remote_total': 64.8035, 'host_total': 7.81372, 'host_system': 7.70424}, 'sum_sent': {'start': 0, 'bits_per_second': 19019900000.0, 'bytes': 2469724160, 'end': 1.0388, 'seconds': 1.0388}, 'streams': [{'sender': {'bits_per_second': 19019900000.0, 'socket': 8, 'end': 1.0388, 'bytes': 2469724160, 'start': 0, 'seconds': 1.0388}, 'receiver': {'bits_per_second': 18984700000.0, 'socket': 8, 'end': 1.0388, 'bytes': 2465153024, 'start': 0, 'seconds': 1.0388}}], 'sum_received': {'start': 0, 'bits_per_second': 18984700000.0, 'bytes': 2465153024, 'end': 1.0388, 'seconds': 1.0388}}}

**Client**

.. code:: python

    >>> import iperf3

    >>> client = iperf3.Client()
    >>> client.duration = 1
    >>> client.server_hostname = '127.0.0.1'
    >>> client.port = 5201
    >>> client.run()
    {'intervals': [{'sum': {'omitted': False, 'bytes': 3905486848, 'start': 0, 'seconds': 1.00005, 'end': 1.00005, 'bits_per_second': 31242500000.0}, 'streams': [{'omitted': False, 'socket': 7, 'bytes': 3905486848, 'start': 0, 'seconds': 1.00005, 'end': 1.00005, 'bits_per_second': 31242500000.0}]}], 'start': {'system_info': 'Linux server.local 2.6.18-408.el5 #1 SMP Fri Dec 11 14:03:08 EST 2015 x86_64 x86_64 x86_64 GNU/Linux\n', 'timestamp': {'time': 'Mon, 15 Aug 2016 14:23:28 GMT', 'timesecs': 1471271008}, 'test_start': {'duration': 1, 'blksize': 131072, 'protocol': 'TCP', 'bytes': 0, 'blocks': 0, 'omit': 0, 'num_streams': 1, 'reverse': 0}, 'version': 'iperf 3.0.6', 'cookie': 'server.local.1471271008', 'connected': [{'local_host': '127.0.0.1', 'remote_host': '127.0.0.1', 'remote_port': 5201, 'socket': 7, 'local_port': 59464}], 'tcp_mss_default': 16384, 'connecting_to': {'host': '127.0.0.1', 'port': 5201}}, 'end': {'cpu_utilization_percent': {'remote_user': 0.0407711, 'host_user': 1.665, 'host_total': 96.216, 'remote_system': 1.83275, 'host_system': 94.4439, 'remote_total': 1.83507}, 'streams': [{'receiver': {'socket': 7, 'bytes': 3905486848, 'start': 0, 'seconds': 1.00005, 'end': 1.00005, 'bits_per_second': 31242500000.0}, 'sender': {'socket': 7, 'bytes': 3905486848, 'start': 0, 'seconds': 1.00005, 'end': 1.00005, 'bits_per_second': 31242500000.0}}], 'sum_sent': {'start': 0, 'seconds': 1.00005, 'end': 1.00005, 'bits_per_second': 31242500000.0, 'bytes': 3905486848}, 'sum_received': {'start': 0, 'seconds': 1.00005, 'end': 1.00005, 'bits_per_second': 31242500000.0, 'bytes': 3905486848}}}

External Dependencies
---------------------

-  iperf3
-  libiperf.0 (should come with iperf3

Testing
-------

- Tested against Ubuntu 14.04 LTS standard iperf3 installation using `travis-ci <https://travis-ci.org/>`__
- Test coverage reporting through `coveralls.io <https://coveralls.io/>`__
- Tested against the following Python versions:
    * 2.7
    * 3.3
    * 3.4
    * 3.5
    * 3.5-dev 
    * nightly

.. |Build Status| image:: https://travis-ci.org/thiezn/iperf3-python.svg?branch=master
   :target: https://travis-ci.org/thiezn/iperf3-python
.. |Coverage Status| image:: https://coveralls.io/repos/github/thiezn/iperf3-python/badge.svg?branch=master
   :target: https://coveralls.io/github/thiezn/iperf3-python?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/iperf3-python/badge/?version=latest
   :target: http://iperf3-python.readthedocs.io/en/latest/?badge=latest
