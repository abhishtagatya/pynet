import json
import socket
import time
import re

import argparse

from pynet.base import BaseRequest


class TCPHandshakeRequest(BaseRequest):
    """
    TCP Handshake Request Object
    """

    def __init__(self, host, port, start_time, end_time, hs_time, sf=False):
        self.host = host
        self.port = port
        self.start_time = start_time
        self.end_time = end_time
        self.hs_time = hs_time

        if sf:
            self.start_time = self.timestamp_to_str(self.start_time)
            self.end_time = self.timestamp_to_str(self.end_time)

    @classmethod
    def measure_hs_time(cls, url_with_port, sf=False):
        """
        Measure Handshake Time between Two Hosts

        :param url_with_port: Arbitrary URL:PORT String
        :param sf: Timestamp String Formatting (False)
        :return: Class Object
        """

        url_with_port = re.sub(r'^https?://', '', url_with_port)

        url, port = url_with_port.split(":", 1)
        port = int(port)
        host, _ = (url + "/").split("/", 1)

        start_time = time.time()

        with socket.create_connection((host, port)) as sock:
            end_time = time.time()

        hs_time = end_time - start_time
        return cls(
            host=host, port=port, start_time=start_time, end_time=end_time, hs_time=hs_time, sf=sf
        )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Measure Handshake Time")
    parser.add_argument("url_with_port", help=f"Arbitrary URL:PORT")
    parser.add_argument("--sf", help=f"Timestamp String Formatting", action="store_true")
    args = parser.parse_args()

    print(TCPHandshakeRequest.measure_hs_time(args.url_with_port, sf=args.sf).to_json())
