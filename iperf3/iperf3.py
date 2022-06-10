"""
Python wrapper for the iperf3 libiperf.so.0 library. The module consists of two
classes, :class:`Client` and :class:`Server`, that inherit from the base class
:class:`IPerf3`. They provide a nice (if i say so myself) and pythonic way to
interact with the iperf3 utility.

At the moment the module redirects stdout and stderr to a pipe and returns the
received data back after each ``client.run()`` or ``server.run()`` call. In
later releases there will be an option to toggle this on or off.

A user should never have to utilise the :class:`IPerf3` class directly, this
class provides common settings for the :class:`Client` and :class:`Server`
classes.

To get started quickly see the :ref:`examples` page.

.. moduleauthor:: Mathijs Mortimer <mathijs@mortimer.nl>
"""
from __future__ import annotations
from ctypes import util, cdll, c_char_p, c_int, c_char, c_void_p, c_uint64
import os
import select
import json
import threading
from socket import SOCK_DGRAM, SOCK_STREAM
from typing import Optional
import warnings
from dacite.core import from_dict
from dacite.exceptions import MissingValueError
from iperf3.iperf3_interfaces import IperfResult

try:
    from queue import Queue
except ImportError:
    from Queue import Queue  # Python2 compatibility


__version__ = "0.1.12"


MAX_UDP_BULKSIZE = 65535 - 8 - 20


def more_data(pipe_out):
    """Check if there is more data left on the pipe

    :param pipe_out: The os pipe_out
    :rtype: bool
    """
    r, _, _ = select.select([pipe_out], [], [], 0)
    return bool(r)


def read_pipe(pipe_out):
    """Read data on a pipe

    Used to capture stdout data produced by libiperf

    :param pipe_out: The os pipe_out
    :rtype: unicode string
    """
    out = b""
    while more_data(pipe_out):
        out += os.read(pipe_out, 1024)

    return out.decode("utf-8")


def output_to_pipe(pipe_in):
    """Redirects stdout and stderr to a pipe

    :param pipe_out: The pipe to redirect stdout and stderr to
    """
    os.dup2(pipe_in, 1)  # stdout
    # os.dup2(pipe_in, 2)  # stderr


def output_to_screen(stdout_fd, stderr_fd):
    """Redirects stdout and stderr to a pipe

    :param stdout_fd: The stdout file descriptor
    :param stderr_fd: The stderr file descriptor
    """
    os.dup2(stdout_fd, 1)
    # os.dup2(stderr_fd, 2)


class IPerf3:
    """The base class used by both the iperf3 :class:`Server` and :class:`Client`

    .. note:: You should not use this class directly
    """

    def __init__(self, role, verbose=True, lib_name=None):
        """Initialise the iperf shared library

        :param role: 'c' = client; 's' = server
        :param verbose: enable verbose output
        :param lib_name: optional name and path for libiperf.so.0 library
        """
        if lib_name is None:
            lib_name = util.find_library("libiperf")
            if lib_name is None:
                # If we still couldn't find it lets try the manual approach
                lib_name = "libiperf.so.0"

        try:
            self.lib = cdll.LoadLibrary(lib_name)
        except OSError:
            raise OSError(f"Couldn't find shared library {lib_name}, is iperf3 installed?")

        # Set the appropriate C types.
        self.lib.iperf_client_end.restype = c_int
        self.lib.iperf_client_end.argtypes = (c_void_p,)
        self.lib.iperf_free_test.restxpe = None
        self.lib.iperf_free_test.argtypes = (c_void_p,)
        self.lib.iperf_new_test.restype = c_void_p
        self.lib.iperf_new_test.argtypes = None
        self.lib.iperf_defaults.restype = c_int
        self.lib.iperf_defaults.argtypes = (c_void_p,)
        self.lib.iperf_get_test_role.restype = c_char
        self.lib.iperf_get_test_role.argtypes = (c_void_p,)
        self.lib.iperf_set_test_role.restype = None
        self.lib.iperf_set_test_role.argtypes = (
            c_void_p,
            c_char,
        )
        self.lib.iperf_get_test_bind_address.restype = c_char_p
        self.lib.iperf_get_test_bind_address.argtypes = (c_void_p,)
        self.lib.iperf_set_test_bind_address.restype = None
        self.lib.iperf_set_test_bind_address.argtypes = (
            c_void_p,
            c_char_p,
        )
        self.lib.iperf_get_test_server_port.restype = c_int
        self.lib.iperf_get_test_server_port.argtypes = (c_void_p,)
        self.lib.iperf_set_test_server_port.restype = None
        self.lib.iperf_set_test_server_port.argtypes = (
            c_void_p,
            c_int,
        )
        self.lib.iperf_get_test_json_output.restype = c_int
        self.lib.iperf_get_test_json_output.argtypes = (c_void_p,)
        self.lib.iperf_set_test_json_output.restype = None
        self.lib.iperf_set_test_json_output.argtypes = (
            c_void_p,
            c_int,
        )
        self.lib.iperf_get_verbose.restype = c_int
        self.lib.iperf_get_verbose.argtypes = (c_void_p,)
        self.lib.iperf_set_verbose.restype = None
        self.lib.iperf_set_verbose.argtypes = (c_void_p, c_int)
        self.lib.iperf_strerror.restype = c_char_p
        self.lib.iperf_strerror.argtypes = (c_int,)
        self.lib.iperf_get_test_server_hostname.restype = c_char_p
        self.lib.iperf_get_test_server_hostname.argtypes = (c_void_p,)
        self.lib.iperf_set_test_server_hostname.restype = None
        self.lib.iperf_set_test_server_hostname.argtypes = (
            c_void_p,
            c_char_p,
        )
        self.lib.iperf_get_test_protocol_id.restype = c_int
        self.lib.iperf_get_test_protocol_id.argtypes = (c_void_p,)
        self.lib.set_protocol.restype = c_int
        self.lib.set_protocol.argtypes = (
            c_void_p,
            c_int,
        )
        self.lib.iperf_get_test_omit.restype = c_int
        self.lib.iperf_get_test_omit.argtypes = (c_void_p,)
        self.lib.iperf_set_test_omit.restype = None
        self.lib.iperf_set_test_omit.argtypes = (
            c_void_p,
            c_int,
        )
        self.lib.iperf_get_test_duration.restype = c_int
        self.lib.iperf_get_test_duration.argtypes = (c_void_p,)
        self.lib.iperf_set_test_duration.restype = None
        self.lib.iperf_set_test_duration.argtypes = (
            c_void_p,
            c_int,
        )
        self.lib.iperf_get_test_rate.restype = c_uint64
        self.lib.iperf_get_test_rate.argtypes = (c_void_p,)
        self.lib.iperf_set_test_rate.restype = None
        self.lib.iperf_set_test_rate.argtypes = (
            c_void_p,
            c_uint64,
        )
        self.lib.iperf_get_test_blksize.restype = c_int
        self.lib.iperf_get_test_blksize.argtypes = (c_void_p,)
        self.lib.iperf_set_test_blksize.restype = None
        self.lib.iperf_set_test_blksize.argtypes = (
            c_void_p,
            c_int,
        )
        self.lib.iperf_get_test_num_streams.restype = c_int
        self.lib.iperf_get_test_num_streams.argtypes = (c_void_p,)
        self.lib.iperf_set_test_num_streams.restype = None
        self.lib.iperf_set_test_num_streams.argtypes = (
            c_void_p,
            c_int,
        )
        self.lib.iperf_has_zerocopy.restype = c_int
        self.lib.iperf_has_zerocopy.argtypes = None
        self.lib.iperf_set_test_zerocopy.restype = None
        self.lib.iperf_set_test_zerocopy.argtypes = (
            c_void_p,
            c_int,
        )
        self.lib.iperf_get_test_reverse.restype = c_int
        self.lib.iperf_get_test_reverse.argtypes = (c_void_p,)
        self.lib.iperf_set_test_reverse.restype = None
        self.lib.iperf_set_test_reverse.argtypes = (
            c_void_p,
            c_int,
        )
        self.lib.iperf_run_client.restype = c_int
        self.lib.iperf_run_client.argtypes = (c_void_p,)
        self.lib.iperf_run_server.restype = c_int
        self.lib.iperf_run_server.argtypes = (c_void_p,)
        self.lib.iperf_reset_test.restype = None
        self.lib.iperf_reset_test.argtypes = (c_void_p,)

        try:
            # Only available from iperf v3.1 and onwards
            self.lib.iperf_get_test_json_output_string.restype = c_char_p
            self.lib.iperf_get_test_json_output_string.argtypes = (c_void_p,)
        except AttributeError:
            pass

        # The test C struct iperf_test
        self._test = self._new()
        self.defaults()

        # stdout/strerr redirection variables
        self._stdout_fd = os.dup(1)
        self._stderr_fd = os.dup(2)
        self._pipe_out, self._pipe_in = os.pipe()  # no need for pipe write

        # Generic test settings
        self.role = role
        self.json_output = True
        self.verbose = verbose

    def __del__(self):
        """Cleanup the test after the :class:`IPerf3` class is terminated"""
        os.close(self._stdout_fd)
        os.close(self._stderr_fd)
        os.close(self._pipe_out)
        os.close(self._pipe_in)

        try:
            # In the current version of libiperf, the control socket isn't
            # closed on iperf_client_end(), see proposed pull request:
            # https://github.com/esnet/iperf/pull/597
            # Workaround for testing, don't ever do this..:
            #
            # sck=self.lib.iperf_get_control_socket(self._test)
            # os.close(sck)

            self.lib.iperf_client_end(self._test)
            self.lib.iperf_free_test(self._test)
        except AttributeError:
            # self.lib doesn't exist, likely because iperf3 wasn't installed or
            # the shared library libiperf.so.0 could not be found
            pass

    def _new(self):
        """Initialise a new iperf test

        struct iperf_test *iperf_new_test()
        """
        return self.lib.iperf_new_test()

    def defaults(self):
        """Set/reset iperf test defaults."""
        self.lib.iperf_defaults(self._test)

    @property
    def role(self):
        """The iperf3 instance role

        valid roles are 'c'=client and 's'=server

        :rtype: 'c' or 's'
        """
        try:
            self._role = c_char(self.lib.iperf_get_test_role(self._test)).value.decode("utf-8")
        except TypeError:
            self._role = c_char(chr(self.lib.iperf_get_test_role(self._test))).value.decode(
                "utf-8"
            )
        return self._role

    @role.setter
    def role(self, role):
        if role.lower() in ["c", "s"]:
            self.lib.iperf_set_test_role(self._test, c_char(role.lower().encode("utf-8")))
            self._role = role
        else:
            raise ValueError("Unknown role, accepted values are 'c' and 's'")

    @property
    def bind_address(self):
        """The bind address the iperf3 instance will listen on

        use * to listen on all available IPs
        :rtype: string
        """
        result = c_char_p(self.lib.iperf_get_test_bind_address(self._test)).value
        if result:
            self._bind_address = result.decode("utf-8")
        else:
            self._bind_address = "*"

        return self._bind_address

    @bind_address.setter
    def bind_address(self, address):
        self.lib.iperf_set_test_bind_address(self._test, c_char_p(address.encode("utf-8")))
        self._bind_address = address

    @property
    def port(self):
        """The port the iperf3 server is listening on"""
        self._port = self.lib.iperf_get_test_server_port(self._test)
        return self._port

    @port.setter
    def port(self, port):
        self.lib.iperf_set_test_server_port(self._test, int(port))
        self._port = port

    @property
    def json_output(self):
        """Toggles json output of libiperf

        Turning this off will output the iperf3 instance results to
        stdout/stderr

        :rtype: bool
        """
        enabled = self.lib.iperf_get_test_json_output(self._test)

        if enabled:
            self._json_output = True
        else:
            self._json_output = False

        return self._json_output

    @json_output.setter
    def json_output(self, enabled):
        if enabled:
            self.lib.iperf_set_test_json_output(self._test, 1)
        else:
            self.lib.iperf_set_test_json_output(self._test, 0)

        self._json_output = enabled

    @property
    def verbose(self):
        """Toggles verbose output for the iperf3 instance

        :rtype: bool
        """
        enabled = self.lib.iperf_get_verbose(self._test)

        if enabled:
            self._verbose = True
        else:
            self._verbose = False

        return self._verbose

    @verbose.setter
    def verbose(self, enabled):
        if enabled:
            self.lib.iperf_set_verbose(self._test, 1)
        else:
            self.lib.iperf_set_verbose(self._test, 0)
        self._verbose = enabled

    @property
    def _errno(self):
        """Returns the last error ID

        :rtype: int
        """
        return c_int.in_dll(self.lib, "i_errno").value

    @property
    def iperf_version(self):
        """Returns the version of the libiperf library

        :rtype: string
        """
        # TODO: Is there a better way to get the const char than allocating 30?
        VersionType = c_char * 30
        return VersionType.in_dll(self.lib, "version").value.decode("utf-8")

    def _error_to_string(self, error_id):
        """Returns an error string from libiperf

        :param error_id: The error_id produced by libiperf
        :rtype: string
        """
        strerror = self.lib.iperf_strerror
        strerror.restype = c_char_p
        return str(strerror(error_id).decode("utf-8"))

    def run(self) -> Optional[IperfResult]:
        """Runs the iperf3 instance.

        This function has to be instantiated by the Client and Server
        instances

        :rtype: NotImplementedError
        """
        raise NotImplementedError


class Client(IPerf3):
    """An iperf3 client connection.

    This opens up a connection to a running iperf3 server

    Basic Usage::

      >>> import iperf3

      >>> client = iperf3.Client()
      >>> client.duration = 1
      >>> client.server_hostname = '127.0.0.1'
      >>> client.port = 5201
      >>> client.run()
      {'intervals': [{'sum': {...
    """

    def __init__(self, *args, **kwargs):
        """Initialise the iperf shared library"""
        super().__init__(role="c", *args, **kwargs)

        # Internal variables
        self._blksize = None
        self._server_hostname = None
        self._port = None
        self._num_streams = None
        self._zerocopy = False
        self._omit = None
        self._duration = None
        self._bandwidth = None
        self._protocol = None

    @property
    def server_hostname(self):
        """The server hostname to connect to.

        Accepts DNS entries or IP addresses.

        :rtype: string
        """
        result = c_char_p(self.lib.iperf_get_test_server_hostname(self._test)).value
        if result:
            self._server_hostname = result.decode("utf-8")
        else:
            self._server_hostname = None
        return self._server_hostname

    @server_hostname.setter
    def server_hostname(self, hostname):
        self.lib.iperf_set_test_server_hostname(self._test, c_char_p(hostname.encode("utf-8")))
        self._server_hostname = hostname

    @property
    def protocol(self):
        """The iperf3 instance protocol

        valid protocols are 'tcp' and 'udp'

        :rtype: str
        """
        proto_id = self.lib.iperf_get_test_protocol_id(self._test)

        if proto_id == SOCK_STREAM:
            self._protocol = "tcp"
        elif proto_id == SOCK_DGRAM:
            self._protocol = "udp"

        return self._protocol

    @protocol.setter
    def protocol(self, protocol):
        if protocol == "tcp":
            self.lib.set_protocol(self._test, int(SOCK_STREAM))
        elif protocol == "udp":
            self.lib.set_protocol(self._test, int(SOCK_DGRAM))

            if self.blksize > MAX_UDP_BULKSIZE:
                self.blksize = MAX_UDP_BULKSIZE

        self._protocol = protocol

    @property
    def omit(self):
        """The test startup duration to omit in seconds."""
        self._omit = self.lib.iperf_get_test_omit(self._test)
        return self._omit

    @omit.setter
    def omit(self, omit):
        self.lib.iperf_set_test_omit(self._test, omit)
        self._omit = omit

    @property
    def duration(self):
        """The test duration in seconds."""
        self._duration = self.lib.iperf_get_test_duration(self._test)
        return self._duration

    @duration.setter
    def duration(self, duration):
        self.lib.iperf_set_test_duration(self._test, duration)
        self._duration = duration

    @property
    def bandwidth(self):
        """Target bandwidth in bits/sec"""
        self._bandwidth = self.lib.iperf_get_test_rate(self._test)
        return self._bandwidth

    @bandwidth.setter
    def bandwidth(self, bandwidth):
        self.lib.iperf_set_test_rate(self._test, bandwidth)
        self._bandwidth = bandwidth

    @property
    def blksize(self):
        """The test blksize."""
        self._blksize = self.lib.iperf_get_test_blksize(self._test)
        return self._blksize

    @blksize.setter
    def blksize(self, bulksize):
        # iperf version < 3.1.3 has some weird bugs when bulksize is
        # larger than MAX_UDP_BULKSIZE
        if self.protocol == "udp" and bulksize > MAX_UDP_BULKSIZE:
            bulksize = MAX_UDP_BULKSIZE

        self.lib.iperf_set_test_blksize(self._test, bulksize)
        self._blksize = bulksize

    @property
    def bulksize(self):
        """The test bulksize.

        Deprecated argument, use blksize instead to ensure consistency
        with iperf3 C library
        """
        # Keeping bulksize argument for backwards compatibility with
        # iperf3-python < 0.1.7
        return self.blksize

    @bulksize.setter
    def bulksize(self, bulksize):
        # Keeping bulksize argument for backwards compatibility with
        # iperf3-python < 0.1.7
        self.blksize = bulksize

    @property
    def num_streams(self):
        """The number of streams to use."""
        self._num_streams = self.lib.iperf_get_test_num_streams(self._test)
        return self._num_streams

    @num_streams.setter
    def num_streams(self, number):
        self.lib.iperf_set_test_num_streams(self._test, number)
        self._num_streams = number

    @property
    def zerocopy(self):
        """Toggle zerocopy.

        Use the sendfile() system call for "Zero Copy" mode. This uses much
        less CPU. This is not supported on all systems.

        **Note** there isn't a hook in the libiperf library for getting the
        current configured value. Relying on zerocopy.setter function

        :rtype: bool
        """
        return self._zerocopy

    @zerocopy.setter
    def zerocopy(self, enabled):
        if enabled and self.lib.iperf_has_zerocopy():
            self.lib.iperf_set_test_zerocopy(self._test, 1)
            self._zerocopy = True
        else:
            self.lib.iperf_set_test_zerocopy(self._test, 0)
            self._zerocopy = False

    @property
    def reverse(self):
        """Toggles direction of test

        :rtype: bool
        """
        enabled = self.lib.iperf_get_test_reverse(self._test)

        if enabled:
            self._reverse = True
        else:
            self._reverse = False

        return self._reverse

    @reverse.setter
    def reverse(self, enabled):
        if enabled:
            self.lib.iperf_set_test_reverse(self._test, 1)
        else:
            self.lib.iperf_set_test_reverse(self._test, 0)

        self._reverse = enabled

    def run(self) -> Optional[IperfResult]:
        """Run the current test client.

        :rtype: instance of :class:`TestResult`
        """
        if self.json_output:
            output_to_pipe(self._pipe_in)  # Disable stdout
            error = self.lib.iperf_run_client(self._test)

            str_data: Optional[str] = None

            if not self.iperf_version.startswith("iperf 3.1"):
                data = read_pipe(self._pipe_out)
                data = str(data)
                if data.startswith("Control connection"):
                    str_data = "{" + data.split("{", 1)[1]
            else:
                data = c_char_p(self.lib.iperf_get_test_json_output_string(self._test)).value
                if data:
                    str_data = data.decode("utf-8")

            output_to_screen(self._stdout_fd, self._stderr_fd)  # enable stdout

            if error or str_data is None:
                return None

            return str_to_iperfresult(str_data)


class Server(IPerf3):
    """An iperf3 server connection.

    This starts an iperf3 server session. The server terminates after each
    successful client connection so it might be useful to run Server.run()
    in a loop.

    The C function iperf_run_server is called in a separate thread to make
    sure KeyboardInterrupt(aka ctrl+c) can still be captured

    Basic Usage::

      >>> import iperf3

      >>> server = iperf3.Server()
      >>> server.run()
      {'start': {...
    """

    def __init__(self, *args, **kwargs):
        """Initialise the iperf3 server instance"""
        super().__init__(role="s", *args, **kwargs)

    def run(self) -> Optional[IperfResult]:
        """Run the iperf3 server instance.

        :rtype: instance of :class:`TestResult`
        """

        def _run_in_thread(self, data_queue):
            """Runs the iperf_run_server

            :param data_queue: thread-safe queue
            """
            output_to_pipe(self._pipe_in)  # disable stdout
            error = self.lib.iperf_run_server(self._test)
            output_to_screen(self._stdout_fd, self._stderr_fd)  # enable stdout

            # TODO json_output_string not available on earlier iperf3 builds
            # have to build in a version check using self.iperf_version
            # The following line should work on later versions:
            # data = c_char_p(
            #    self.lib.iperf_get_test_json_output_string(self._test)
            # ).value
            data = read_pipe(self._pipe_out)

            if not data or error:
                data = '{"error": "%s"}' % self._error_to_string(self._errno)

            self.lib.iperf_reset_test(self._test)
            data_queue.put(data)

        if self.json_output:
            data_queue = Queue()

            t = threading.Thread(target=_run_in_thread, args=[self, data_queue])
            t.daemon = True

            t.start()
            while t.is_alive():
                t.join(0.1)

            str_data = str(data_queue.get())
            return str_to_iperfresult(str_data)
        else:
            # setting json_output to False will output test to screen only
            self.lib.iperf_run_server(self._test)
            self.lib.iperf_reset_test(self._test)

            return None


def str_to_iperfresult(str_data: str) -> Optional[IperfResult]:
    json_data = json.loads(str_data)
    try:
        typed_data = from_dict(data_class=IperfResult, data=json_data)
        return typed_data
    except MissingValueError as e:
        warnings.warn(f"{e}. Returning result as 'None'")
        return None
