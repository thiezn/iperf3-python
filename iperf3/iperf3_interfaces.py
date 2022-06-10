from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List

# Generated https://json2pyi.pages.dev/#Dataclass


@dataclass
class IperfResult:
    start: Start
    intervals: List[Interval]
    end: End


@dataclass
class Start:
    connected: List[Connected]
    version: str
    system_info: str
    timestamp: Timestamp
    connecting_to: Optional[ConnectingTo]
    cookie: str
    tcp_mss_default: int
    test_start: TestStart


@dataclass
class Connected:
    socket: int
    local_host: str
    local_port: int
    remote_host: str
    remote_port: int


@dataclass
class Timestamp:
    time: str
    timesecs: int


@dataclass
class ConnectingTo:
    host: str
    port: int


@dataclass
class TestStart:
    protocol: str
    num_streams: int
    blksize: int
    omit: int
    duration: int
    bytes: int
    blocks: int
    reverse: int


@dataclass
class Interval:
    streams: List[IperfStream]
    sum: SumReceivedOrSumSentOrSumOrReceiverOrSender


@dataclass
class IperfStream:
    socket: int
    start: float
    end: float
    seconds: float
    bytes: int
    bits_per_second: float
    retransmits: Optional[int]
    snd_cwnd: Optional[int]
    omitted: bool


@dataclass
class SumReceivedOrSumSentOrSumOrReceiverOrSender:
    start: float
    end: float
    seconds: float
    bytes: int
    bits_per_second: float
    retransmits: Optional[int]
    omitted: Optional[bool]
    socket: Optional[int]


@dataclass
class End:
    streams: List[SendReceiveStreamer]
    sum_sent: SumReceivedOrSumSentOrSumOrReceiverOrSender
    sum_received: SumReceivedOrSumSentOrSumOrReceiverOrSender
    cpu_utilization_percent: CpuUtilizationPercent


@dataclass
class SendReceiveStreamer:
    sender: SumReceivedOrSumSentOrSumOrReceiverOrSender
    receiver: SumReceivedOrSumSentOrSumOrReceiverOrSender


@dataclass
class CpuUtilizationPercent:
    host_total: float
    host_user: float
    host_system: float
    remote_total: float
    remote_user: float
    remote_system: float
