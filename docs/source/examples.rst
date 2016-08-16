.. _examples:

Examples
========

Full client options
~~~~~~~~~~~~~~~~~~~

>>> import iperf3

>>> client = iperf3.Client()
>>> client.duration = 1
>>> client.bind_address = '10.0.0.1'
>>> client.server_hostname = '10.10.10.10'
>>> client.port = 6969
>>> client.bulksize = 1234
>>> client.num_streams = 10
>>> client.zerocopy = True
>>> client.verbose = False
>>> client.run()
