"""Wrapper for the iperf3 libiperf.so.0 library

library explanation and examples using man libiperf
"""

from ctypes import cdll, c_char_p, c_int, c_char
import os
import select
import json

__version__ = '0.1'


def more_data(pipe_out):
    r, _, _ = select.select([pipe_out], [], [], 0)
    return bool(r)


def read_pipe(pipe_out):
    out = b''
    while more_data(pipe_out):
        out += os.read(pipe_out, 1024)

    return out.decode('utf-8')


class IPerf3(object):
    def __init__(self,
                 role='s',
                 json_output=True,
                 verbose=True,
                 iperf_version='3.0.6',
                 lib_name='libiperf.so.0'):
        """Initialise the iperf shared library

        :param library: The libiperf library providing the API to iperf3
        """
        # TODO see if we can determine the iperf3 version. for instance
        # iperf3.1 supports output to file and iperf_test_output_json_string
        self.iperf_version = iperf_version

        # TODO use find_library to find the best library
        self.lib = cdll.LoadLibrary(lib_name)

        # The test C struct iperf_test
        self._test = self._new()
        self.defaults()

        # Generic test settings
        self.role = role
        self.json_output = json_output
        self.verbose = verbose

        # Internal variables
        self._bulksize = None
        self._server_hostname = None
        self._server_port = None
        self._num_streams = None
        self._zerocopy = False

    def __del__(self):
        """Cleanup the test after the IPerf3 class is terminated"""
        self.lib.iperf_free_test(self._test)

    def _new(self):
        """Initialise a new iperf test

        struct iperf_test *iperf_new_test()
        """
        return self.lib.iperf_new_test()

    def defaults(self):
        """(Re)set iperf test defaults

        int iperf_defaults(struct iperf_test *t);
        """
        self.lib.iperf_defaults(self._test)

    # TODO use the iperf getter functions to retrieve
    # the actual configured data and sync it up with the
    # python variables

    @property
    def role(self):
        """Get the role

        :return s (for server) or c (for client)
        """
        return self._role

    @role.setter
    def role(self, role):
        """Set the role

        :param role: c or s ('c=client, s=server')

        void iperf_set_test_role( struct iperf_test *pt, char role );
        """
        if role.lower() in ['c', 's']:
            self.lib.iperf_set_test_role(self._test,
                                         c_char(role.lower().encode('utf-8')))
            self._role = role
        else:
            raise ValueError("Unknown role, accepted values are 'c' and 's'")

    @property
    def bind_address(self):
        """Get the bind address"""
        return self._bind_address

    @bind_address.setter
    def bind_address(self, address):
        """Set the bind address

        :param address: address to bind on, * for any available address

        void iperf_set_test_bind_address( struct iperf_test *t, char *bind_address );
        """
        self.lib.iperf_set_test_bind_address(self._test,
                                             c_char_p(address.encode('utf-8')))
        self._bind_address = address

    @property
    def server_hostname(self):
        """Get the server hostname"""
        return self._server_hostname

    @server_hostname.setter
    def server_hostname(self, hostname):
        """Set the server hostname

        void iperf_set_test_server_hostname( struct iperf_test *t, char *server_host );
        """
        self.lib.iperf_set_test_server_hostname(self._test,
                                                c_char_p(hostname.encode('utf-8')))
        self._server_hostname = hostname

    @property
    def server_port(self):
        """Get the server port"""
        return self._server_port

    @server_port.setter
    def server_port(self, port):
        """Set the server port

        void iperf_set_test_server_port( struct iperf_test *t, int server_port );
        """
        self.lib.iperf_set_test_server_port(self._test, int(port))
        self._server_port = port

    @property
    def duration(self):
        """Get the test duration"""
        return self._duration

    @duration.setter
    def duration(self, duration):
        """Set the test duration

        void iperf_set_test_duration( struct iperf_test *t, int duration );
        """
        self.lib.iperf_set_test_duration(self._test, duration)
        self._duration = duration

    @property
    def bulksize(self):
        """Get the test bulksize"""
        return self._bulksize

    @bulksize.setter
    def bulksize(self, bulksize):
        """Set the test bulksize

        void iperf_set_test_blksize( struct iperf_test *t, int blksize );
        """
        self.lib.iperf_set_test_blksize(self._test, bulksize)
        self._bulksize = bulksize

    @property
    def num_streams(self):
        """Get the number of streams"""
        return self._num_streams

    @num_streams.setter
    def num_streams(self, number):
        """Set the number of streams

        void iperf_set_test_num_streams( struct iperf_test *t, int num_streams );
        """
        self.lib.iperf_set_test_num_streams(self._test, number)
        self._num_streams = number

    @property
    def json_output(self):
        """Toggle json output"""
        return self._json_output

    @json_output.setter
    def json_output(self, enabled):
        """Toggle json output

        void iperf_set_test_json_output( struct iperf_test *t, int json_output );
        """
        if enabled:
            self.lib.iperf_set_test_json_output(self._test, 1)
        else:
            self.lib.iperf_set_test_json_output(self._test, 0)

        self._json_output = enabled

    @property
    def verbose(self):
        """Toggle verbose output"""
        return self._verbose

    @verbose.setter
    def verbose(self, enabled):
        """Toggle verbose output

        iperf_set_verbose(  struct iperf_test *t, int ? );
        """
        if enabled:
            self.lib.iperf_set_verbose(self._test, 1)
        else:
            self.lib.iperf_set_verbose(self._test, 0)
        self._verbose = enabled

    @property
    def zerocopy(self):
        """Get the zerocopy value"""

        # TODO This is not working as expected, perhaps need
        # to ensure the return is indeed 1
        """
        if self.lib.iperf_has_zerocopy() == 1:
            self._zerocopy = True
        else:
            self._zerocopy = False
        """
        return self._zerocopy

    @zerocopy.setter
    def zerocopy(self, enabled):
        """Set the zerocopy

        Use the sendfile() system call for "Zero Copy" mode. This uses much
        less CPU.

        void iperf_set_test_zerocopy( struct iperf_test* t, int zerocopy );
        """
        if enabled:
            self.lib.iperf_set_test_zerocopy(self._test, 1)
        else:
            self.lib.iperf_set_test_zerocopy(self._test, 0)

        self._zerocopy = enabled

    @property
    def _errno(self):
        """Returns the last error ID"""
        return c_int.in_dll(self.lib, "i_errno").value

    def _error_to_string(self, error_id):
        """Returns an error string if available"""
        strerror = self.lib.iperf_strerror
        strerror.restype = c_char_p
        return strerror(error_id)

    def run(self):
        """Run the current test client

        int iperf_run_client(struct iperf_test *);
        int iperf_run_server(struct iperf_test *);
        """

        # Redirect stdout to a pipe to capture the libiperf output
        pipe_out, pipe_in = os.pipe()
        stdout = os.dup(1)
        os.dup2(pipe_in, 1)

        if self.role == 'c':
            error = self.lib.iperf_run_client(self._test)
            if error:
                print(self._error_to_string(self._errno))
            else:
                # redirect stdout back to normal and parse received data
                os.dup2(stdout, 1)
                data = json.loads(read_pipe(pipe_out))
                print(data)

        elif self.role == 's':
            while True:
                self.lib.iperf_run_server(self._test)

                # redirect stdout back to normal and parse received data
                os.dup2(stdout, 1)
                data = json.loads(read_pipe(pipe_out))
                print(data)
                os.dup2(pipe_in, 1)

                self.lib.iperf_reset_test(self._test)
