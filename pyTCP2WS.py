#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import sys
import argparse
import logging
from queue import Queue

# Local packages
from lib.TCPServer import JSONServer
from lib.WebSocketServer import HTTPServer


def parse_args(params):
    """ Parse cmd line arguments """
    parser = argparse.ArgumentParser(
        description="Send your data from TCP socket to WebSocket using JSON")

    # Set parameters
    parser.add_argument("--tcp-port", action="store",
                        help="Specify TCP port to listen for JSON packets")
    parser.add_argument("--ws-port", action="store",
                        help="Specify WebSocket port to send JSON data to")
    parser.add_argument("--host", action="store", default="127.0.0.1",
                        help="Specify host to bind socket on")
    args = parser.parse_args(params)

    return args


def main(params):
    # Global logging settings
    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s - %(levelname)s - [%(name)s] - %(message)s")

    # Init in queue (producer and consumer pattern)
    in_queue = Queue()

    # Set default host
    host = params.host if params.host else "127.0.0.1"

    # Start JSON server
    if params.tcp_port:
        tcp_server = JSONServer(host, int(params.tcp_port), in_queue)
        tcp_server.start()

    # Start WebSocket server
    if params.ws_port:
        http_server = HTTPServer(host, int(params.ws_port), in_queue)
        http_server.start()

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args)

# EOF
