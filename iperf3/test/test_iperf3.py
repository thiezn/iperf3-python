from iperf3 import IPerf3
import pytest


class TestPyPerf:

    def test_start_client(self):
        client = IPerf3(role='c')
        assert client._test

    def test_client_role(self):
        client = IPerf3(role='c')
        assert client._test

    def test_server_role(self):
        server = IPerf3(role='s')
        assert server._test

    def test_incorrect_role(self):
        with pytest.raises(ValueError):
            IPerf3(role='bla')

    def test_bind_address(self):
        """Test setting of the bind address is properly passed
        on to the iperf3 API"""
        client = IPerf3(role='c')
        client.bind_address = '127.0.0.1'
        assert client.bind_address == '127.0.0.1'

    def test_server_port(self):
        server = IPerf3()
        server.server_port = 666
        assert server.server_port == 666

    def test_server_hostname(self):
        server = IPerf3()
        server.server_hostname = 'localhost'
        assert server.server_hostname == 'localhost'

    def test_duration(self):
        client = IPerf3(role='c')
        client.duration = 666
        assert client.duration == 666

    def test_bulksize(self):
        client = IPerf3(role='c')
        client.bulksize = 666
        assert client.bulksize == 666

    def test_num_streams(self):
        client = IPerf3(role='c')
        client.num_streams = 666
        assert client.num_streams == 666

    def test_json_output_enabled(self):
        client = IPerf3(role='c')
        client.json_output = True
        assert client.json_output

    def test_json_output_disabled(self):
        client = IPerf3(role='c')
        client.json_output = False
        assert not client.json_output

    def test_verbose_enabled(self):
        client = IPerf3(role='c')
        client.verbose = True
        assert client.verbose

    def test_verbose_disabled(self):
        client = IPerf3(role='c')
        client.verbose = False
        assert not client.verbose

    def test_zerocopy_enabled(self):
        client = IPerf3(role='c')
        client.zerocopy = True
        assert client.zerocopy

    def test_zerocopy_disabled(self):
        client = IPerf3(role='c')
        client.zerocopy = False
        assert not client.zerocopy

    def test_get_last_error(self):
        client = IPerf3(role='c')
        assert client._errno == 0

    def test_error_to_string(self):
        client = IPerf3(role='c')
        assert client._error_to_string(1) == b'cannot be both server and client'
