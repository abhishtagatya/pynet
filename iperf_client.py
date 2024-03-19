#!/usr/bin/env python3

import json
import argparse

from pynet.base import BaseRequest

import iperf3


class Iperf3ClientHeader(BaseRequest):
    """
    Iperf3 Client Header Object
    """

    def __init__(self, 
            remote_addr, remote_port, 
            version, sys_info,
            num_streams, blksize, duration,
            ctype='TCP'):
        self.remote_addr = remote_addr
        self.remote_port = remote_port
        self.version = version
        self.sys_info = sys_info
        self.ctype = ctype
        self.num_streams = num_streams
        self.blksize = blksize
        self.duration = duration



class Iperf3ResourceUtilization(BaseRequest):

    def __init__(self, host_total, host_user, host_system, remote_total, remote_user, remote_system):
        self.host_total = host_total
        self.host_user = host_user
        self.host_system = host_system
        self.remote_total = remote_total
        self.remote_user = remote_user
        self.remote_system = remote_system



class Iperf3TCPSummarySent(BaseRequest):

    def __init__(self, 
            start, end, 
            seconds, bps, sbytes,
            retransmits, sender=True):
        self.start = start
        self.end = end
        self.seconds = seconds
        self.bps = bps
        self.bytes = sbytes
        self.retransmits = retransmits
        self.sender = sender


class Iperf3TCPSummaryReceived(BaseRequest):
    
    def __init__(self, start, end, seconds, bps, rbytes, sender=True):
        self.start = start
        self.end = end
        self.seconds = seconds
        self.bps = bps
        self.bytes = rbytes
        self.sender = sender


class Iperf3TCPClientRequest(BaseRequest):

    def __init__(self, 
            sent_summary: Iperf3TCPSummarySent, 
            received_summary: Iperf3TCPSummaryReceived, 
            sender_congestion, receiver_congestion, 
            header=None, resource=None):
        self.sent_summary = sent_summary
        self.received_summary = received_summary
        self.sender_congestion = sender_congestion
        self.receiver_congestion = receiver_congestion
        self.header = header
        self.resource = resource

    
    @classmethod
    def connect(cls, remote_addr, remote_port, duration=1, blksize=1234, num_streams=1):
        client = iperf3.Client()
        client.server_hostname = remote_addr
        client.port = remote_port
        client.duration = duration
        client.blksize = blksize
        client.num_streams = num_streams

        result = client.run()
        result = result.json
        header = Iperf3ClientHeader(
            remote_addr=result["start"]["connecting_to"]["host"],
            remote_port=result["start"]["connecting_to"]["port"],
            version=result["start"]["version"],
            sys_info=result["start"]["system_info"],
            num_streams=result["start"]["test_start"]["num_streams"],
            blksize=result["start"]["test_start"]["blksize"],
            duration=result["start"]["test_start"]["duration"]
        )
        resource = Iperf3ResourceUtilization(
            host_total=result["end"]["cpu_utilization_percent"]["host_total"],
            host_user=result["end"]["cpu_utilization_percent"]["host_user"],
            host_system=result["end"]["cpu_utilization_percent"]["host_system"],
            remote_total=result["end"]["cpu_utilization_percent"]["remote_total"],
            remote_user=result["end"]["cpu_utilization_percent"]["remote_user"],
            remote_system=result["end"]["cpu_utilization_percent"]["remote_system"],
        )
        sent_sum = Iperf3TCPSummarySent(
            start=result["end"]["sum_sent"]["start"],
            end=result["end"]["sum_sent"]["end"],
            seconds=result["end"]["sum_sent"]["seconds"],
            sbytes=result["end"]["sum_sent"]["bytes"],
            bps=result["end"]["sum_sent"]["bits_per_second"],
            retransmits=result["end"]["sum_sent"]["retransmits"],
            sender=result["end"]["sum_sent"]["sender"],
        )
        recv_sum = Iperf3TCPSummaryReceived(
            start=result["end"]["sum_received"]["start"],
            end=result["end"]["sum_received"]["end"],
            seconds=result["end"]["sum_received"]["seconds"],
            bps=result["end"]["sum_received"]["bits_per_second"],
            rbytes=result["end"]["sum_received"]["bytes"],
            sender=result["end"]["sum_received"]["sender"],
        )
        sender_congestion = result["end"]["sender_tcp_congestion"]
        receiver_congestion = result["end"]["receiver_tcp_congestion"]


        return cls(sent_sum, recv_sum, sender_congestion, receiver_congestion, header=header, resource=resource)

    def to_json(self):
        return json.dumps({
            "header": self.header.__dict__,
            "summary": {
                "sent": self.sent_summary.__dict__,
                "received": self.received_summary.__dict__
            },
            "sender_tcp_congestion": self.sender_congestion,
            "receiver_tcp_congestion": self.receiver_congestion,
            "resource": self.resource.__dict__,
        })


if __name__ =='__main__':
    parser = argparse.ArgumentParser(description="Iperf3 Client Test")
    parser.add_argument("address", help=f"Iperf3 Server Address")
    parser.add_argument("port", help=f"Iperf3 Server Port")
    parser.add_argument("conn", help=f"Connection Type")
    args = parser.parse_args()

    if args.conn == "udp":
        pass
    else:
        print(Iperf3TCPClientRequest.connect(args.address, args.port).to_json())
