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

Soon you will be able to do the following

.. code-block:: bash

    pip install iperf3

But for now the only option is install manually from github:

.. code-block:: bash

    git clone https://github.com/thiezn/iperf3-python.git
    cd iperf3-python
    python3 setup.py test  # Optional testing of module using py.test (or py.test through tox)
    python3 setup.py install
