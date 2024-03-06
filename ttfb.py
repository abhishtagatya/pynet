import json
import socket
import time
import re

import argparse


class TTFBRequest:
    """
    TTFB (Time To First Byte) Request Object
    """

    def __init__(self, url, byte, start_time, end_time, fb_time):
        self.url = url
        self.byte = byte
        self.start_time = start_time
        self.end_time = end_time
        self.fb_time = fb_time

    @classmethod
    def measure_ttfb(cls, url, byte=1024):
        """
        Measure TTFB (Time to First Byte(s)).

        :param url: Arbitrary URL String
        :param byte: Measurement of a Byte (1024)
        :return: Class Object
        """

        url = re.sub(r'^https?://', '', url)

        host, path = (url + "/").split("/", 1)
        path = "/" + path

        # Create a socket connection to the host
        with socket.create_connection((host, 80)) as sock:
            request = f"GET {path} HTTP/1.1\r\nHost:{host}\r\nConnection: close\r\n\r\n"
            start_time = time.time()

            sock.sendall(request.encode())

            resp = b""
            while True:
                chunk = sock.recv(byte)

                if len(chunk) == 0:
                    break

                resp += chunk

                if len(resp) >= byte:
                    break

            end_time = time.time()

        ttfb = end_time - start_time
        return cls(url=url, byte=byte, start_time=start_time, end_time=end_time, fb_time=ttfb)

    def to_json(self):
        return json.dumps(self.__dict__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Measure TTBF (Time To First Byte)")
    parser.add_argument("url", help=f"Arbitrary URL")
    parser.add_argument("-byte", help=f"Measurement of a Byte", required=False, default=1024)
    args = parser.parse_args()

    print(TTFBRequest.measure_ttfb(url=args.url, byte=int(args.byte)).to_json())
