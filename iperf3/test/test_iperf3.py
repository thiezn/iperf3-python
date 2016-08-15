from iperf3 import IPerf3

class TestPyPerf:

    def test_start_client(self):
        client = IPerf3(role='c')
        assert client._test
