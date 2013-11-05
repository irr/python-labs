import gevent
from gevent import socket
from gevent import monkey

monkey.patch_all()

import sys

def greenlet(port):
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', port))
    s.listen(500)
    while True:
        conn, addr = s.accept()
        gevent.spawn(handle_request, conn)

def handle_request(conn):
    try:
        data = conn.recv(8192)
        request = data.splitlines()
        if len(request) > 0 and request[-1] == "":
            print "request: ", request
            do_proxy(conn, data)
        conn.shutdown(socket.SHUT_WR)
    except Exception as ex:
        print ex
    finally:
        conn.close()

def do_proxy(conn, data):
    try:
        remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote.connect(("localhost", 8888))
        remote.send(data)
        while True:
            bytes = remote.recv(8192)
            if bytes:
                conn.send(bytes)
            else:
                break
        remote.shutdown(socket.SHUT_WR)
    except Exception as ex:
        print ex
    finally:
        remote.close()

if __name__ == '__main__':
    greenlet(int(sys.argv[1]))