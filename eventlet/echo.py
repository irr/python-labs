import eventlet

def handle(fd):
    print "client connected"
    while True:
        # pass through every non-eof line
        x = fd.readline()
        if not x: break
        fd.write(x)
        fd.flush()
        print "echoed", x,
    print "client disconnected"

print "server socket listening on port 6000"
server = eventlet.listen(('0.0.0.0', 6000))
pool = eventlet.GreenPool()
while True:
    try:
        new_sock, address = server.accept()
        print "accepted", address
        pool.spawn_n(handle, new_sock.makefile('rw'))
    except (SystemExit, KeyboardInterrupt):
        break