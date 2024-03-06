import json
import socket
import time
import re

import argparse


class TCPHandshakeRequest:

    def __init__(self, host, port, start_time, end_time, hs_time):
        self.host = host
        self.port = port
        self.start_time = start_time
        self.end_time = end_time
        self.hs_time = hs_time

    @classmethod
    def measure_hs_time(cls, url_with_port):
        """
        Measure Handshake Time between Two Hosts

        :param url_with_port: Arbitrary URL:PORT String
        :return: Class Object
        """

        url_with_port = re.sub(r'^https?://', '', url_with_port)

        host, port = url_with_port.split(":", 1)
        host = host.replace('/', '')
        port = int(port)

        start_time = time.time()

        with socket.create_connection((host, port)) as sock:
            end_time = time.time()

        hs_time = end_time - start_time
        return cls(host=host, port=port, start_time=start_time, end_time=end_time, hs_time=hs_time)

    def to_json(self):
        return json.dumps(self.__dict__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Measure Handshake Time")
    parser.add_argument("url_with_port", help=f"Arbitrary URL:PORT")
    args = parser.parse_args()

    print(TCPHandshakeRequest.measure_hs_time(args.url_with_port).to_json())
