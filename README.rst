iperf3-python: Python wrapper around iperf3
===========================================

|PyPi Status| |Build Status| |Coverage Status| |Documentation Status|

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

**note** The libiperf API was only introduced in 3.0.6 so make sure you have an updated version
of iperf3 installation.

- Install from source (preferred)

.. code:: bash

    wget http://downloads.es.net/pub/iperf/iperf-3-current.tar.gz
    tar xvf iperf-3-current.tar.gz
    cd iperf-3.1.3/                # Or whatever the latest version is
    ./configure && make && sudo make install

- Ubuntu:

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

For detailed examples check out the `examples page <http://iperf3-python.readthedocs.io/en/latest/examples.html>`__ or
the detailed documentation at `iperf3-python.readthedocs.org <https://iperf3-python.readthedocs.org/>`__


**Server**

.. code:: python

    >>> import iperf3

    >>> server = iperf3.Server()
    >>> result = server.run()
    >>> result.remote_host
    "10.10.10.10"

**Client**

.. code:: python

    >>> import iperf3

    >>> client = iperf3.Client()
    >>> client.duration = 1
    >>> client.server_hostname = '127.0.0.1'
    >>> client.port = 5201
    >>> result = client.run()
    >>> result.sent_Mbps
    32583.293914794922


External Dependencies
---------------------

-  iperf3
-  libiperf.so.0 (Comes with iperf3 >= 3.0.6)

Testing
-------

- Tested against the following iperf3 versions on Unix (ubuntu Trusty):

  - 3.0.6
  - 3.0.7
  - 3.0.8
  - 3.0.9
  - 3.0.10
  - 3.0.11
  - 3.0.12
  - 3.1
  - 3.1.1
  - 3.1.2
  - 3.1.3

- Test coverage reporting through `coveralls.io <https://coveralls.io/>`__
- Tested against the following Python versions:

  - 2.7
  - 3.6

.. |PyPi Status| image:: https://img.shields.io/pypi/v/iperf3.svg
   :target: https://pypi.python.org/pypi/iperf3
.. |Build Status| image:: https://travis-ci.org/thiezn/iperf3-python.svg?branch=master
   :target: https://travis-ci.org/thiezn/iperf3-python
.. |Coverage Status| image:: https://coveralls.io/repos/github/thiezn/iperf3-python/badge.svg?branch=master
   :target: https://coveralls.io/github/thiezn/iperf3-python?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/iperf3-python/badge/?version=latest
   :target: http://iperf3-python.readthedocs.io/en/latest/?badge=latest
