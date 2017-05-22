# CSM117_Project

Currently working on the Server side for our CSM117 "Get the Booty" Project. The Server was previously started in regular Python but
was updated to Twisted Python. Good resources to learn how to build Twisted Python servers are found below:
https://media.readthedocs.org/pdf/twisted/latest/twisted.pdf
http://twistedmatrix.com/documents/13.0.0/core/howto/servers.html
https://www.raywenderlich.com/3932/networking-tutorial-for-ios-how-to-create-a-socket-based-iphone-app-and-server

Here are some steps highlighting the progress of the server in Twisted Python so far:
1. The ServerFactory class is listening on a TCP socket on a specified port.
2. When a client connection is made, the ServerFactory class creates an instance of a Server class, 
and saves clients currently connected to the server
