import gevent
import gnsq
import simplejson as json

from gevent import monkey

monkey.patch_all()


# rm -rf q?;mkdir q1 q2
# nsqd --data-path ./q1 --tcp-address=0.0.0.0:4150 --http-address=0.0.0.0:4151 --lookupd-tcp-address=0.0.0.0:4160
# nsqd --data-path ./q2 --tcp-address=0.0.0.0:5150 --http-address=0.0.0.0:5151 --lookupd-tcp-address=0.0.0.0:4160
# nsqlookupd -broadcast-address 127.0.0.1
# nsqadmin --lookupd-http-address=0.0.0.0:4161

# http://localhost:4171/nodes

def consumer(ports=[4150, 5150]):
    reader = gnsq.Reader("topic", "channel",
                         lookupd_http_addresses=["localhost:4161"],
                         nsqd_tcp_addresses=["localhost:{0}".format(port) for port in ports])

    @reader.on_message.connect
    def handler(server, message):
        msg = "got message from {0}={1}".format(server, message.body.decode("utf-8"))
        print("(C)>>> {0}: {1}".format(server, msg))
    reader.start()


def producer(port=4151, sleep=1, loop=2):
    conn = gnsq.Nsqd(address='localhost', http_port=port)
    for n in range(loop):
        msg = "gevent test {0} sent to {1}!".format(n, port)
        print("(P)>>> {0}: {1}".format(producer, msg))
        conn.publish('topic', json.dumps({"msg": msg, "id": n}))
        gevent.sleep(sleep)


if __name__ == "__main__":
    cons = gevent.spawn(consumer)
    prod = [gevent.spawn(producer, port) for port in [4151, 5151]]
    gevent.joinall(prod)
    gevent.kill(cons)

