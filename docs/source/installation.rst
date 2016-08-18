.. _installation:

Installation
============

To be able to utilise the python wrapper around iperf3 you will need to have the
libiperf.so.0 shared library installed. Luckily this comes with the standard iperf3
build.

**warnings** the iperf3 python wrapper is not yet published on PyPi (aka pip install)


iperf3 utility
~~~~~~~~~~~~~~

Preferably get the latest build from the iperf3 `official website <http://software.es.net/iperf/>`__

Otherwise try your OS package manager:

- Ubuntu 14.04 LTS:

.. code-block:: bash

    sudo apt-get install iperf3

- CentOS/RedHat

.. code-block:: bash

    sudo yum install iperf3


iperf3 python wrapper
~~~~~~~~~~~~~~~~~~~~~

The preferred installation method is through PyPi (aka pip install)

.. code-block:: bash

    pip install iperf3

If pip is unavailable for any reason you can also manually install from github:

.. code-block:: bash

    git clone https://github.com/thiezn/iperf3-python.git
    cd iperf3-python
    python3 setup.py test  # (optional) testing through py.test and/or tox
    python3 setup.py install
