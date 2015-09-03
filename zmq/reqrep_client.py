import zmq
import sys

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

context = zmq.Context()
print "Connecting to server..."
socket = context.socket(zmq.REQ)
print("connecting to tcp://localhost:%s" % (port,))
socket.connect ("tcp://localhost:%s" % port)
if len(sys.argv) > 2:
    print("connecting to tcp://localhost:%s" % (port1,))
    socket.connect ("tcp://localhost:%s" % port1)

#  Do 10 requests, waiting each time for a response
for request in range (1,10):
    print "Sending request ", request,"..."
    socket.send ("Hello")
    #  Get the reply.
    message = socket.recv()
    print "Received reply ", request, "[", message, "]"

# Demo:
# python reqrep_server.py 5546
# python reqrep_server.py 5556
# python reqrep_client.py 5546 5556