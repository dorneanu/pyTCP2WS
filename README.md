Motivation
----------

During my [D3](http://d3js.org/) experiments  I wanted to capture data from the command line and send it to my D3 application. Of course I could have read the data from some CSV,JSON file but that wasn't "real-time" enough. So I had a 

* data source
* D3 code applying some magic to the data 

The *data source* in that case were some grep lines transformed to JSON data. In fact I was missing the linking part between mentioned components.  

Basic idea
------

*pyTCP2WS* listens for some data on a **TCP** socket and passes it through some **WebSocket**. At the moment only JSON data is supported.

In order to transfer data from one socket to the another a (deadlock free) queue is being used (producer and consumer pattern).


Run me
-------

These are the basic parameters:

    $ python3 pyTCP2WS.py --help
	usage: pyTCP2WS.py [-h] [--tcp-port TCP_PORT] [--ws-port WS_PORT]
	                   [--host HOST]

	Send your data from TCP socket to WebSocket using JSON

	optional arguments:
	  -h, --help           show this help message and exit
	  --tcp-port TCP_PORT  Specify TCP port to listen for JSON packets
	  --ws-port WS_PORT    Specify WebSocket port to send JSON data to
	  --host HOST          Specify host to bind socket on

In order to start a TCP socket to pass-through your JSON data to your web socket, run:

	$ python3 pyTCP2WS.py --tcp-port 8081 --ws-port 8080 
	2014-03-04 18:14:19,245 - INFO - [TCPServer] - Listening on 8081
	2014-03-04 18:14:19,247 - INFO - [HTTPServer] - Starting HTTP server on port 8080
	2014-03-04 18:14:19,247 - INFO - [HTTPServer] - Start collector server
	2014-03-04 18:14:19,247 - INFO - [HTTPServer] - Waiting for incoming data ...

Now using you can send data to the TCP socket:

	$ echo '{"value":"30"}' | json | nc localhost 8081

Now you should see pyTCP2WS printing some debug messages:

	...
	2014-03-04 18:15:39,068 - INFO - [TCPServer] - Added JSON to IN queue
	2014-03-04 18:15:39,068 - INFO - [HTTPServer] - Received data!
