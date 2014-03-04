#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import socketserver
import json
import logging

from queue import Queue
from threading import Thread


class TCPServer(socketserver.ThreadingTCPServer):
    """ Custom TCP server """
    def __init__(self, server_address, RequestHandlerClass, in_queue=Queue()):
        # Set queues
        self.in_queue = in_queue

        # Call parents constructor
        super(TCPServer, self).__init__(server_address, RequestHandlerClass)

        # Avoid "address already in use" error
        socketserver.ThreadingTCPServer.allow_reuse_address = True
        self.allow_reuse_address = True

        # Logging settings
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger("TCPServer")
        self.logger.setLevel(logging.INFO)


class TCPServerHandler(socketserver.BaseRequestHandler):
    """ Waiting for incoming (JSON) data """
    def handle(self):
        try:
            # Wait for data
            data = json.loads(self.request.recv(1024).decode('UTF-8').strip())

            # Process data
            self.process_data(data)

        except Exception as e:
            print("Exception wile receiving message: ", e)
            self.request.sendall(bytes(json.dumps({'return': 'error'}), 'UTF-8'))

    def process_data(self, data):
        """ Process received data """
        self.server.in_queue.put(data)
        self.server.in_queue.task_done()
        self.server.logger.info("Added JSON to IN queue")


class JSONServer():
    """ TCP Server waiting for JSON packets """

    def __init__(self, host, port, in_queue=Queue()):
        # Global settings
        self.host = host
        self.port = port

        # Init super class
        self.server = TCPServer((self.host, self.port), TCPServerHandler, in_queue)

    def start(self):
        """ Start JSON server """
        self.server.logger.info("Listening on %s" % self.port)
        server_thread = Thread(target=self.server.serve_forever)
        server_thread.start()
