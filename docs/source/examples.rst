.. _examples:

Examples
========

Check the examples/ folder for a few ready to go python scripts.

Client
~~~~~~

**Example 1**

This example sets up a client connection to a running server on 10.10.10.10:6969.
When the test finalises the results are returned. This example shows all currently
available options for a :class:`Client <iperf3.Client>`

>>> import iperf3

>>> client = iperf3.Client()
>>> client.omit = 1
>>> client.duration = 1
>>> client.bind_address = '10.0.0.1'
>>> client.server_hostname = '10.10.10.10'
>>> client.port = 6969
>>> client.blksize = 1234
>>> client.num_streams = 10
>>> client.zerocopy = True
>>> client.verbose = False
>>> client.reverse = True
>>> client.run()
{'start': {'test_start': {...

**Example 2**

This example shows how you can output the client test results to screen, just like
the iperf3 application itself does. Note it does NOT return a :class:`TestResult <iperf3.TestResult>`
instance.

>>> import iperf3

>>> client = iperf3.Client()
>>> client.server_hostname = '10.10.10.10'
>>> client.port = 6969
>>> client.json_output = False
>>> result = client.run()
Time: Mon, 15 May 2017 18:20:01 GMT
Connecting to host 10.10.10.10, port 6969
[  8] local 127.0.0.1 port 35670 connected to 127.0.0.1 port 5201
Starting Test: protocol: TCP, 1 streams, 131072 byte blocks, omitting 0 seconds, 1 second test
[ ID] Interval           Transfer     Bandwidth       Retr  Cwnd
[  8]   0.00-1.00   sec  3.96 GBytes  34.0 Gbits/sec    0   3.18 MByt...

>>> result
None

**Example 3**

Here is an example of running a UDP test. Please read the official documentation on
UDP testing as there can be a few catches.

.. literalinclude:: ../../examples/udp_client.py
   :language: python

Server
~~~~~~

**Example 1**

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
