from gevent import socket
from gevent.server import StreamServer

# this handler will be run for each incoming connection in a dedicated greenlet
def echo(socket, address):
    print ('New connection from %s:%s' % address)
    socket.sendall('Welcome to the echo server! Type quit to exit.\r\n'.encode('ascii'))
    # using a makefile because we want to use readline()
    fileobj = socket.makefile(mode='rw')
    while True:
        line = fileobj.readline()
        if not line:
            print ("client disconnected")
            break
        if line.strip().lower() == 'quit':
            print ("client quit")
            break
        fileobj.write(line)
        fileobj.flush()
        print ("echoed %r" % line)


if __name__ == '__main__':
    # to make the server use SSL, pass certfile and keyfile arguments to the constructor
    server = StreamServer(('0.0.0.0', 6000), echo)
    # to start the server asynchronously, use its start() method;
    # we use blocking serve_forever() here because we have no other jobs
    print ('Starting echo server on port 6000')
    server.serve_forever()
