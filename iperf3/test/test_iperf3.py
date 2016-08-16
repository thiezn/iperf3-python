import iperf3
import pytest
import subprocess
from time import sleep


class TestPyPerf:

    def test_init_client(self):
        client = iperf3.Client()
        assert client._test

    def test_init_server(self):
        server = iperf3.Server()
        assert server._test

    def test_incorrect_role(self):
        with pytest.raises(ValueError):
            iperf3.IPerf3(role='bla')

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

    def test_server_hostname(self):
        server = iperf3.Server()
        server.server_hostname = 'localhost'
        assert server.server_hostname == 'localhost'

    def test_duration(self):
        client = iperf3.Client()
        client.duration = 666
        assert client.duration == 666

    def test_bulksize(self):
        client = iperf3.Client()
        client.bulksize = 666
        assert client.bulksize == 666

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

    def test_get_last_error(self):
        client = iperf3.Client()
        assert client._errno == 0

    def test_error_to_string(self):
        client = iperf3.Client()
        assert client._error_to_string(1) == 'cannot be both server and client'

    def test_client_run(self):
        client = iperf3.Client()
        client.server_hostname = '127.0.0.1'
        client.port = 6969
        client.duration = 1
        response = client.run()
        assert response == {'error': 'unable to connect to server: Connection refused'}

    def test_client_succesful_run(self):
        client = iperf3.Client()
        client.server_hostname = '127.0.0.1'
        client.port = 5201
        client.duration = 1

        server = subprocess.Popen(["iperf3", "-s"])
        sleep(.3)  # give the server some time to start
        response = client.run()
        server.kill()

        assert response['start']['connecting_to'] == {'host': '127.0.0.1', 'port': 5201}
