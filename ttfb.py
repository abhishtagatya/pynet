import json
import socket
import time
import re

import argparse

from pynet.base import BaseRequest


class TTFBRequest(BaseRequest):
    """
    TTFB (Time To First Byte) Request Object
    """

    def __init__(self, url, start_time, end_time, fb_time, sf=False):
        super(TTFBRequest, self).__init__()

        self.url = url
        self.start_time = start_time
        self.end_time = end_time
        self.fb_time = fb_time

        if sf:
            self.start_time = self.timestamp_to_str(self.start_time)
            self.end_time = self.timestamp_to_str(self.end_time)

    @classmethod
    def measure_ttfb(cls, url, sf=False):
        """
        Measure TTFB (Time to First Byte(s)).

        :param url: Arbitrary URL String
        :param sf: Timestamp String Formatting (False)
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
                chunk = sock.recv(1024)

                if len(chunk) == 0:
                    break

                resp += chunk

                if len(resp) >= 1024:
                    break

            end_time = time.time()

        ttfb = end_time - start_time
        return cls(
            url=url, start_time=start_time, end_time=end_time, fb_time=ttfb, sf=sf
        )

    def to_json(self):
        return json.dumps(self.__dict__)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Measure TTBF (Time To First Byte)")
    parser.add_argument("url", help=f"Arbitrary URL")
    parser.add_argument("--sf", help=f"Timestamp String Formatting", action="store_true")
    args = parser.parse_args()

    print(TTFBRequest.measure_ttfb(url=args.url, sf=args.sf).to_json())
