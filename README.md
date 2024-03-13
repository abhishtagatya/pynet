# PyNET
> Simple Networking Scripts

### Quick Start

Required modules
- Python 3.8+
- Socket (built-in)
- Argparse (built-in)
- iperf

### Installation

#### Iperf

```shell
sudo apt-get install iperf3 && pip3 install iperf3
```

### Scripts

#### TCP Handshake Time
Measuring the time to establish a TCP/UDP connection between two hosts.

```shell
python handshake.py https://www.google.com:443
```

#### TTFB (Time to First Byte)
Measuring the time from the client making an HTTP request to the first byte of the page being received by the browser.

```shell
python ttfb.py https://github.com
```

#### Downloaded Bytes
Measuring the total amount of data downloaded during a test session.

```shell
python download.py https://fit.vut.cz
```
