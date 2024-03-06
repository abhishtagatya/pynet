import json
import socket
import ssl
import time
import re

import argparse

from pynet.base import BaseRequest


class DownloadSizeRequest(BaseRequest):
    """
    Download Size Request Object
    """

    def __init__(self, url, start_time, end_time, download_time, total_bytes, sf=False):
        super(DownloadSizeRequest, self).__init__()

        self.url = url
        self.start_time = start_time
        self.end_time = end_time
        self.download_time = download_time
        self.total_bytes = total_bytes

        if sf:
            self.start_time = self.timestamp_to_str(self.start_time)
            self.end_time = self.timestamp_to_str(self.end_time)

    @classmethod
    def measure_download_size(cls, url, chunk=1024, sf=False):
        """
        Measure Download Size and Time

        :param url: Arbitrary URL String
        :param chunk: Chunk Size (1024)
        :param sf: Timestamp String Formatting (False)
        :return: Class Object
        """

        use_https = url.startswith("https://")
        url = re.sub(r'^https?://', '', url)

        host, path = (url + "/").split("/", 1)
        path = "/" + path

        port = 443 if use_https else 80

        with socket.create_connection((host, port)) as sock:
            if use_https:
                sock = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLS)

            request = f"GET {path} HTTP/1.1\r\nHost:{host}\r\nConnection: close\r\n\r\n"
            start_time = time.time()

            sock.sendall(request.encode())

            total_bytes = 0
            while True:
                chunk_rcv = sock.recv(chunk)
                if not chunk_rcv:
                    break
                total_bytes += len(chunk_rcv)
            end_time = time.time()
            download_time = end_time - start_time

            return cls(
                url=url, start_time=start_time, end_time=end_time, download_time=download_time,
                total_bytes=total_bytes, sf=sf
            )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Measure TTBF (Time To First Byte)")
    parser.add_argument("url", help=f"Arbitrary URL")
    parser.add_argument("--chunk", help=f"Chunk Size Per Iteration", required=False, default=1024)
    parser.add_argument("--sf", help=f"Timestamp String Formatting", action="store_true")
    args = parser.parse_args()

    print(DownloadSizeRequest.measure_download_size(url=args.url, chunk=int(args.chunk), sf=args.sf).to_json())
