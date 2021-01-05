import os
import iperf3
import pytest
import subprocess
import base64
import re
from time import sleep

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

# Return paths files local to this module.
# Given file, assumed to be in directory as this module, transform it into the full path to find it.
def get_test_data_file_path(file):
  dirname = os.path.dirname(os.path.abspath(__file__))
  x= os.path.join(dirname, file)
  print(x)
  return x

# Return the contents of a PEM file Base 64 encoded
# And yes, if you're wondering the "key" part of the PEM
# file is already Base64 encoded. Turns out the iperf_api is funky
# and assumes the file to be "double" encoded.
def get_key_as_base64(key_file):
    with open(get_test_data_file_path(key_file), 'rb') as file:
        raw_key = file.read()
        return base64.b64encode(raw_key).decode("ascii")

# Return (major, minor, mini) tuple of version from version string
# like iperf 3.2.1.
# Return 3.0.0 if the version string is poorly formed.
def get_iperf_version(version_string):
    match = re.match(r"iperf ([0-9])\.([0-9]).([0-9])", version_string)
    return (int(match[1]), int(match[2]), int(match[3])) if match else (3, 0, 0)

class TestPyPerf:

    def test_init_client(self):
        client = iperf3.Client()
        assert client._test

    def test_init_server(self):
        server = iperf3.Server()
        assert server._test

    def test_lib_name(self):
        client = iperf3.Client()
        assert client._test

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

    def test_protocol_property(self):
        client = iperf3.Client()
        assert client.protocol == 'tcp'

        client.protocol = 'udp'
        assert client.protocol == 'udp'

        client.protocol = 'tcp'
        assert client.protocol == 'tcp'

    def test_udp_blksize_limit(self):
        """Ensure the blksize can't exceed MAX_UDP_BULKSIZE"""
        MAX_UDP_BULKSIZE = (65535 - 8 - 20)
        client = iperf3.Client()
        client.protocol = 'udp'

        client.blksize = MAX_UDP_BULKSIZE + 10
        assert client.blksize == MAX_UDP_BULKSIZE

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
        assert client.server_hostname == '127.0.0.1'

    def test_omit(self):
        client = iperf3.Client()
        client.omit = 666
        assert client.omit == 666

    def test_duration(self):
        client = iperf3.Client()
        client.duration = 666
        assert client.duration == 666

    def test_iperf3_version(self):
        client = iperf3.Client()
        assert 'iperf' in client.iperf_version

    def test_blksize(self):
        client = iperf3.Client()
        client.blksize = 666
        assert client.blksize == 666

    def test_bandwidth(self):
        client = iperf3.Client()
        client.bandwidth = 1
        assert client.bandwidth == 1

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
        print(client._error_to_string(client._errno))
        assert client._errno == 111

    def test_error_to_string(self):
        client = iperf3.Client()
        assert client._error_to_string(1) == 'cannot be both server and client'

    def test_client_failed_run(self):
        client = iperf3.Client()
        client.server_hostname = '127.0.0.1'
        client.port = 5201
        client.duration = 1
        response = client.run()
        assert "unable to connect to server" in response.error

    def test_client_succesful_run(self):
        client = iperf3.Client()
        client.server_hostname = '127.0.0.1'
        client.port = 5202
        client.duration = 1

        server = subprocess.Popen(["iperf3", "-s", "-p", "5202"])
        sleep(.3)  # give the server some time to start
        response = client.run()
        server.kill()

        assert response.remote_host == '127.0.0.1'
        assert response.remote_port == 5202

        # These are added to check some of the TestResult variables
        assert not response.reverse
        assert response.type == 'client'
        assert response.__repr__()

    def test_client_succesful_run_reverse(self):
        client = iperf3.Client()
        client.server_hostname = '127.0.0.1'
        client.port = 5203
        client.duration = 1
        client.reverse = True

        server = subprocess.Popen(["iperf3", "-s", "-p", "5203"])
        sleep(.3)  # give the server some time to start
        response = client.run()
        server.kill()

        assert response.remote_host == '127.0.0.1'
        assert response.remote_port == 5203

        # These are added to check some of the TestResult variables
        assert response.reverse
        assert response.type == 'client'
        assert response.__repr__()

    def test_client_succesful_run_udp(self):
        client = iperf3.Client()
        client.protocol = 'udp'
        client.server_hostname = '127.0.0.1'
        client.port = 5204
        client.duration = 1

        server = subprocess.Popen(["iperf3", "-s", "-p", "5204"])
        sleep(.3)  # give the server some time to start
        response = client.run()
        server.kill()

        assert response.remote_host == '127.0.0.1'
        assert response.remote_port == 5204

        # These are added to check some of the TestResult variables
        assert not response.reverse
        assert response.type == 'client'
        assert response.__repr__()

    def test_server_failed_run(self):
        """This test will launch two server instances on the same ip:port
        to generate an error"""
        server = iperf3.Server()
        server.bind_address = '127.0.0.1'
        server.port = 5201
        print("here")
        server2 = subprocess.Popen(["iperf3", "-s"])
        sleep(.3)  # give the server some time to start
        print("server started")
        response = server.run()
        server2.kill()

        assert "unable to start listener for connections: " in response.error

    def test_server_run(self):
        server = iperf3.Server()
        server.bind_address = '127.0.0.1'
        server.port = 5205

        # Launching the client with a sleep timer to give our server some time to start
        client = subprocess.Popen(
            'sleep .5 && iperf3 -c 127.0.0.1 -p 5205 -t 1',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        response = server.run()

        (major, minor, mini) = get_iperf_version(server.iperf_version)
        if  major >= 3 and minor >= 0:
            assert not response.error
            assert response.local_host == '127.0.0.1'
            assert response.local_port == 5205
            assert response.type == 'server'
        else:
            assert response.error == 'the client has unexpectedly closed the connection'


    def test_server_run_output_to_screen(self):
        server = iperf3.Server()
        server.bind_address = '127.0.0.1'
        server.port = 5206
        server.json_output = False

        # Launching the client with a sleep timer to give our server some time to start
        client = subprocess.Popen(
            'sleep .5 && iperf3 -c 127.0.0.1 -p 5206 -t 1',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        response = server.run()
        client.kill()

        assert not response

    def test_client_succesful_run_output_to_screen(self):
        """Test if we print iperf3 test output to screen when json_output = False."""
        client = iperf3.Client()
        client.server_hostname = '127.0.0.1'
        client.port = 5207
        client.duration = 1
        client.json_output = False

        server = subprocess.Popen(["iperf3", "-s", "-p", "5207"])
        sleep(.3)  # give the server some time to start
        response = client.run()
        server.kill()

        assert response == None

    def test_client_succesful_run_udp_output_to_screen(self):
        """Test if we print iperf3 test output to screen when json_output = False."""
        client = iperf3.Client()
        client.protocol = 'udp'
        client.server_hostname = '127.0.0.1'
        client.port = 5208
        client.duration = 1
        client.json_output = False

        server = subprocess.Popen(["iperf3", "-s", "-p", "5208"])
        sleep(.3)  # give the server some time to start
        response = client.run()
        server.kill()

        assert response == None

    def test_result(self):
        dirname = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(dirname, 'results.json')) as f:
            json = f.read()

        result = iperf3.TestResult(json)
        assert result.sent_bps  == 935992000
        assert result.sent_kbps == 935992
        assert result.sent_Mbps == 935.992
        assert isclose(result.sent_kB_s, 114256.836, rel_tol=0.01)
        assert isclose(result.sent_MB_s, 111.579, rel_tol=0.01)

        assert result.received_bps  == 934268000
        assert result.received_kbps  == 934268
        assert result.received_Mbps  == 934.268

        assert isclose(result.received_kB_s, 114046.387, rel_tol=0.01)
        assert isclose(result.received_MB_s, 111.373, rel_tol=0.01)

    def test_client_successful_run_with_auth(self):
        client = iperf3.Client()
        client.server_hostname = '127.0.0.1'
        client.port = 5209
        client.duration = 1
        client.username = "test"
        client.password = "test"
        client.rsa_pubkey = get_key_as_base64("public.pem")

        server = subprocess.Popen(["iperf3", "-s", "-p", "5209", "--authorized-users-path", get_test_data_file_path("authorized_users.txt"),
            "--rsa-private-key-path", get_test_data_file_path("private_not_protected.pem")])
        sleep(.3)  # give the server some time to start
        response = client.run()
        server.kill()

        print(response)
        assert response.remote_host == '127.0.0.1'
        assert response.remote_port == 5209

        # These are added to check some of the TestResult variables
        assert not response.reverse
        assert response.type == 'client'
        assert response.__repr__()

    def test_client_failed_run_with_auth(self):
        client = iperf3.Client()
        client.server_hostname = '127.0.0.1'
        client.port = 5210
        client.duration = 1
        client.username = "test"
        client.password = "wrongpassword"
        client.rsa_pubkey = get_key_as_base64("public.pem")

        server = subprocess.Popen(["iperf3", "-s", "-p", "5210", "--authorized-users-path", get_test_data_file_path("authorized_users.txt"),
            "--rsa-private-key-path", get_test_data_file_path("private_not_protected.pem")])
        sleep(.3)  # give the server some time to start
        response = client.run()
        server.kill()

        assert "test authorization failed" in response.error

    def test_server_run_with_auth(self):
        server = iperf3.Server()
        server.bind_address = '127.0.0.1'
        server.port = 5211
        # Use authorized_users.txt, public.pem, private.pem and
        # username/password of test/test for client / server auth
        server.authorized_users = get_test_data_file_path("authorized_users.txt")
        server.rsa_privkey = get_key_as_base64("private_not_protected.pem")

        # Launching the client with a sleep timer to give our server some time to start
        client = subprocess.Popen(
            'sleep .3 && iperf3 -c 127.0.0.1 -p 5211 -t 1 --rsa-public-key-path ' + get_test_data_file_path("public.pem") + ' --username test',
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={'IPERF3_PASSWORD': 'test'}
        )
        response = server.run()

        (major, minor, mini) = get_iperf_version(server.iperf_version)
        if  major >= 3 and minor >= 8:
            assert not response.error
            assert response.local_host == '127.0.0.1'
            assert response.local_port == 5211
            assert response.type == 'server'
        else:
            assert response.error == 'the client has unexpectedly closed the connection'
