.. _installation:

Installation
============

To be able to utilise the python wrapper around iperf3 you will need to have the
libiperf.so.0 shared library installed. Luckily this comes with the standard iperf3
build.


iperf3 utility
~~~~~~~~~~~~~~

Preferably get the latest build from the iperf3 `official website <http://software.es.net/iperf/>`__

Otherwise try your OS package manager:

- Ubuntu:

.. code-block:: bash

    sudo apt-get install iperf3

- CentOS/RedHat

.. code-block:: bash

    sudo yum install iperf3


iperf3 python wrapper
~~~~~~~~~~~~~~~~~~~~~

The preferred installation method is through PyPi (aka pip install)

.. code-block:: bash

    # Using Poetry
    poetry add git+https://github.com/Greenroom-Robotics/iperf3-python.git

    # Using Pip
    pip install git+https://github.com/Greenroom-Robotics/iperf3-python.git

If pip is unavailable for any reason you can also manually install from github:

.. code-block:: bash

    git clone https://github.com/Greenroom-Robotics/iperf3-python
    cd iperf3-python
    python3 setup.py test  # (optional) testing through py.test and/or tox
    python3 setup.py install
