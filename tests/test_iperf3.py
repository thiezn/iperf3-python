import iperf3
import pytest
import subprocess
from time import sleep
from socket import SOCK_DGRAM, SOCK_STREAM
from iperf3.iperf3 import MAX_UDP_BULKSIZE


class TestPyPerf:

    def test_unavailable_library(self):
        with pytest.raises(OSError):
            client = iperf3.Client(lib_name='bla')

    def test_init_client(self):
        client = iperf3.Client()
        assert client._test

    def test_init_server(self):
        server = iperf3.Server()
        assert server._test

    def test_run_not_implemented(self):
        with pytest.raises(NotImplementedError):
            client = iperf3.IPerf3(role='c')
            client.run()

    def test_incorrect_role(self):
        with pytest.raises(ValueError):
            iperf3.IPerf3(role='bla')

    def test_role_property(self):
        client = iperf3.Client()
        assert client.role == 'c'

    def test_bind_address_empty(self):
        """Test if we bind to any/all address when empty bind_address is
        passed"""
        client = iperf3.Client()
        client.bind_address = ''
        assert client.bind_address == '*'

    def test_bind_address(self):
        """Test setting of the bind address is properly passed
        on to the iperf3 API"""
        client = iperf3.Client()
        client.bind_address = '127.0.0.1'
        assert client.bind_address == '127.0.0.1'

    def test_port(self):
        server = iperf3.Server()
        server.port = 666
        assert server.port == 666

    def test_server_hostname_empty(self):
        client = iperf3.Client()
        client.server_hostname = ''
        assert client.server_hostname == None

    def test_server_hostname(self):
        client = iperf3.Server()
        client.server_hostname = '127.0.0.1'
        print(client.server_hostname)
        assert client.server_hostname == '127.0.0.1'

    def test_duration(self):
        client = iperf3.Client()
        client.duration = 666
        assert client.duration == 666

    def test_iperf3_version(self):
        client = iperf3.Client()
        assert 'iperf' in client.iperf_version

    def test_bulksize(self):
        client = iperf3.Client()
        client.bulksize = 666
        assert client.bulksize == 666

    def test_protocol(self):
        client = iperf3.Client()
        client.protocol = SOCK_DGRAM
        assert client.protocol == SOCK_DGRAM

    def test_wrong_bulksize_for_udp(self):
        client = iperf3.Client()
        client.protocol = SOCK_DGRAM
        client.bulksize = MAX_UDP_BULKSIZE + 1
        assert client.bulksize <= MAX_UDP_BULKSIZE

    def test_num_streams(self):
        client = iperf3.Client()
        client.num_streams = 666
        assert client.num_streams == 666

    def test_json_output_enabled(self):
        client = iperf3.Client()
        client.json_output = True
        assert client.json_output

    def test_json_output_disabled(self):
        client = iperf3.Client()
        client.json_output = False
        assert not client.json_output

    def test_verbose_enabled(self):
        client = iperf3.Client()
        client.verbose = True
        assert client.verbose

    def test_verbose_disabled(self):
        client = iperf3.Client()
        client.verbose = False
        assert not client.verbose

    def test_zerocopy_enabled(self):
        client = iperf3.Client()
        client.zerocopy = True
        assert client.zerocopy

    def test_zerocopy_disabled(self):
        client = iperf3.Client()
        client.zerocopy = False
        assert not client.zerocopy

    def test_reverse_enabled(self):
        client = iperf3.Client()
        client.reverse = True
        assert client.reverse

    def test_reverse_disabled(self):
        client = iperf3.Client()
        client.reverse = False
        assert not client.reverse

    def test_get_last_error(self):
        client = iperf3.Client()
        assert client._errno == 0

    def test_error_to_string(self):
        client = iperf3.Client()
        assert client._error_to_string(1) == 'cannot be both server and client'

    def test_client_failed_run(self):
        client = iperf3.Client()
        client.server_hostname = '127.0.0.1'
        client.port = 5201
        client.duration = 1
        response = client.run()
        assert response.error == "unable to connect to server: Connection refused"

    def test_client_succesful_run(self):
        client = iperf3.Client()
        client.server_hostname = '127.0.0.1'
        client.port = 5201
        client.duration = 1

        server = subprocess.Popen(["iperf3", "-s"])
        sleep(.3)  # give the server some time to start
        response = client.run()
        server.kill()

        assert response.remote_host == '127.0.0.1'
        assert response.remote_port == 5201

        # These are added to check some of the TestResult variables
        assert not response.reverse
        assert response.type == 'client'
        assert response.__repr__()

    def test_udp_client_succesful_run(self):
        client = iperf3.Client()
        client.server_hostname = '127.0.0.1'
        client.port = 5201
        client.duration = 1
        client.protocol = SOCK_DGRAM

        server = subprocess.Popen(["iperf3", "-s"])
        sleep(.3)  # give the server some time to start
        response = client.run()
        server.kill()

        assert response.remote_host == '127.0.0.1'
        assert response.remote_port == 5201

        # These are added to check some of the TestResult variables
        assert not response.reverse
        assert response.type == 'client'
        assert response.protocol == 'UDP'
        assert response.__repr__()


    def test_server_failed_run(self):
        """This test will launch two server instances on the same ip:port
        to generate an error"""
        server = iperf3.Server()
        server.bind_address = '127.0.0.1'
        server.port = 5201

        server2 = subprocess.Popen(["iperf3", "-s"])
        sleep(.3)  # give the server some time to start

        response = server.run()
        server2.kill()

        assert "unable to start listener for connections: " in response.error

    def test_server_run(self):
        server = iperf3.Server()
        server.bind_address = '127.0.0.1'
        server.port = 5201

        # Launching the client with a sleep timer to give our server some time to start
        client = subprocess.Popen('sleep .5 && iperf3 -c 127.0.0.1 5201 -t 1',
                                  shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        response = server.run()
        client.kill()

        assert not response.error
        assert response.local_host == '127.0.0.1'
        assert response.local_port == 5201
