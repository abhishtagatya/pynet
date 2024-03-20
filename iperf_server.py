import iperf3

import argparse

class IperfServer():

    def __init__(self, bind_addr='127.0.0.1', port='9631', verbose=False):
        self.bind_addr = bind_addr
        self.port = port
        self.verbose = verbose

    def run(self):
        server = iperf3.Server()
        server.bind_address = self.bind_addr
        server.port = self.port
        server.verbose = self.verbose

        print(f"Starting to Server at {self.bind_addr}:{self.port}")
        while True:
            print(server.run().json)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create an Iperf Server")
    parser.add_argument("--address", help=f"Bind Address (127.0.0.1)", default="127.0.0.1")
    parser.add_argument("--port", help=f"Bind Address Port (9631)", default="9631")
    parser.add_argument("--v", help="Verbose Output", action="store_true")
    args = parser.parse_args()

    ipfServer = IperfServer(bind_addr=args.address, port=args.port, verbose=args.v)

    try:
        ipfServer.run()
    except KeyboardInterrupt:
        print(f"Server Stopped : {ipfServer}")
