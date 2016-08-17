iperf3 - Python interface to iperf3 using the libiperf API

Documentation on `readthedocs.org`_

|Build Status| |Coverage Status| |Documentation Status|

Description
-----------

iperf3 for python provides a wrapper around the excellent iperf3
utility. iperf3 is a complete rewrite of the original iperf
implementation. more information on the `official iperf3 site`_

iperf3 introduced an API called libiperf that allows you to easily
interact with iperf3 from other languages. This library provides a
python wrapper around libiperf for easy integration into your own python
scripts in a pythonic way

Installation
------------

Make sure iperf3 is present on your system. Installation on Ubuntu 14.04
LTS:

::

    sudo apt-get install iperf3

NOTE: module not yet published on PyPi so pip install not available yet.

::

    pip install iperf3

From github:

::

    git clone https://github.com/thiezn/iperf3-python.git
    cd iperf3-python
    python3 setup.py install

Server
~~~~~~

\`\`\`python >>> import iperf3

            server = iperf3.Server() server.run() {‘start’:
            {‘accepted\_connection’: {‘host’: ‘127.0.0.1’, ‘port’:
            45995}, ‘version’: ‘iperf 3.0.6’, ‘timestamp’: {‘timesecs’:
            1471333681, ‘time’: ‘Tue, 16 Aug 2016 07:48:01 GMT’},
            ‘connected’: [{‘local\_host’: ‘127.0.0.1’, ‘local\_port’:
            5201, ‘socket’: 8, ‘remote\_port’: 45996, ‘remote\_host’:
            ‘127.0.0.1’}], ‘tcp\_mss\_default’: 16384, ‘system\_info’:
            ‘Linux server.local 2.6.18-408.el5 #1 SMP Fri Dec 11
            14:03:08 EST 2015 x86\_64 x86\_64 x86\_64
            GNU/Linux:raw-latex:`\n`’, ‘test\_start’: {‘num\_streams’:
            1, ‘blksize’: 131072, ‘omit’: 0, ‘protocol’: ‘TCP’, ‘bytes’:
            0, ‘blocks’: 0, ‘duration’: 1, ‘reverse’: 0}, ‘cookie’:
            ‘server.local.1471333681’}, ‘intervals’: [{‘streams’:
            [{‘bits\_per\_second’: 18954200000.0, ‘socket’: 8, ‘end’:
            1.00009, ‘omitted’: False, ‘bytes’: 2369470464, ‘start’: 0,
            ‘seconds’: 1.00009}], ‘sum’: {‘omitted’: False,
            ‘bits\_per\_second’: 18954200000.0, ‘end’: 1.00009, ‘bytes’:
            2369470464, ‘start’: 0, ‘seconds’: 1.00009}}, {‘streams’:
            [{‘bits\_per\_second’: 19773800000.0, ‘socket’: 8, ‘end’:
            1.0388, ‘omitted’: False, ‘bytes’: 95682560, ‘start’:
            1.00009, ‘seconds’: 0.0387108}], ‘sum’: {‘omitted’: False,
            ‘bits\_per\_second’: 19773800000.0, ‘end’: 1.0388, ‘bytes’:
            95682560, ‘start’: 1.00009, ‘seconds’: 0.0387108}}], ‘end’:
            {‘cpu\_utilization\_percent’: {‘remote\_user’: 1.75867,
            ‘remote\_system’: 63.1275, ‘host\_user’: 0.0386741,
            ‘remote\_total’: 64.8035, ‘host\_total’: 7.81372,
            ‘host\_system’: 7.70424}, ‘sum\_sent’: {‘start’: 0,
            ‘bits\_per\_second’: 19019900000.0, ‘bytes’: 2469724160,
            ‘end’: 1.0388, ‘seconds’: 1.0388}, ‘streams’

.. _readthedocs.org: https://iperf3-python.readthedocs.org/
.. _official iperf3 site: https://iperf.fr/

.. |Build Status| image:: https://travis-ci.org/thiezn/iperf3-python.svg?branch=master
   :target: https://travis-ci.org/thiezn/iperf3-python
.. |Coverage Status| image:: https://coveralls.io/repos/github/thiezn/iperf3-python/badge.svg?branch=master
   :target: https://coveralls.io/github/thiezn/iperf3-python?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/iperf3-python/badge/?version=latest
   :target: http://iperf3-python.readthedocs.io/en/latest/?badge=latest
