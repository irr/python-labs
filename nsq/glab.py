import gevent
import gnsq
import simplejson as json

from gevent import monkey

monkey.patch_all()


# rm -rf q?;mkdir q1 q2
# nsqd --data-path ./q1 --tcp-address=0.0.0.0:4150 --http-address=0.0.0.0:4151 --lookupd-tcp-address=0.0.0.0:4160
# nsqd --data-path ./q2 --tcp-address=0.0.0.0:4250 --http-address=0.0.0.0:4251 --lookupd-tcp-address=0.0.0.0:4160
# nsqlookupd -broadcast-address 127.0.0.1
# nsqadmin --lookupd-http-address=0.0.0.0:4161

# http://localhost:4171/nodes

# alias nsqlookup='docker run --name lookupd --rm -p 4160:4160 -p 4161:4161 nsqio/nsq /nsqlookupd'
# alias nsqdc='rm -rf /opt/nosql/nsqd/data?/*'
# alias nsqd1='docker run --name nsqd1 --rm --net host -v /opt/nosql/nsqd/data1:/data -p 4150:4150 -p 4151:4151 nsqio/nsq /nsqd --broadcast-address=127.0.0.1 --lookupd-tcp-address=127.0.0.1:4160 --http-address=0.0.0.0:4151 --tcp-address=0.0.0.0:4150 --data-path=/data'
# alias nsqd2='docker run --name nsqd2 --rm --net host -v /opt/nosql/nsqd/data2:/data -p 4250:4250 -p 4251:4251 nsqio/nsq /nsqd --broadcast-address=127.0.0.2 --lookupd-tcp-address=127.0.0.1:4160 --http-address=0.0.0.0:4251 --tcp-address=0.0.0.0:4250 --data-path=/data'
# alias nsqadmin='docker run --name nsqadmin --rm --net host -p 4171:4171 nsqio/nsq /nsqadmin --lookupd-http-address=127.0.0.1:4161'

# curl -d "<message>" http://127.0.0.1:4151/pub?topic=topic

def consumer():
    reader = gnsq.Reader("topic", "channel",
                         max_in_flight=10,
                         max_concurrency=-1,
                         lookupd_http_addresses=['127.0.0.1:4161'])
    @reader.on_message.connect
    def handler(server, message):
        msg = "got message from {0}={1}".format(server, message.body.decode("utf-8"))
        print("(C)>>> {0}: {1}".format(server, msg))
    reader.start()


def producer(port=4151, sleep=1, loop=10):
    conn = gnsq.Nsqd(address='localhost', http_port=port)
    for n in range(loop):
        msg = "gevent test {0} sent to {1}!".format(n, port)
        print("(P)>>> {0}: {1}".format(producer, msg))
        conn.publish('topic', json.dumps({"msg": msg, "id": n}))
        gevent.sleep(sleep)


if __name__ == "__main__":
    cons = [gevent.spawn(consumer)]
    prod = [gevent.spawn(producer, port) for port in [4151, 4251]]
    gevent.joinall(prod)
    gevent.joinall(cons)

