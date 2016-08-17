.. _examples:

Examples
========

Client
~~~~~~

This example sets up a client connection to a running server on 10.10.10.10:6969.
When the test finalises the results are returned. This example shows all currently
available options for a :class:`Client <iperf3.Client>`

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
{'start': {'test_start': {...

Server
~~~~~~

This example runs an iperf3 server on 10.10.10.10:6969 and prints out the test results.
After each test ``server.run()`` finishes and produces the test results. This example
shows all currently available options for a :class:`Server <iperf3.Server>`

>>> import iperf3

>>> server = iperf3.Server()
>>> server.bind_address = '10.10.10.10'
>>> server.port = 6969
>>> server.verbose = False
>>> while True:
...     server.run()
...
{'start': {'test_start': {...
