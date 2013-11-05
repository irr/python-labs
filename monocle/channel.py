import sys
import monocle
from monocle import _o
monocle.init("tornado")

from monocle.stack import eventloop
from monocle.experimental import Channel

@_o
def main():
    s = 2
    ch = Channel(s)
    for i in xrange(s):
        print i
        yield ch.send(i)

    print ch.bufsize, len(ch._msgs)
    for i in xrange(s):
        print (yield ch.recv())
    print "done"
    sys.exit(0)

monocle.launch(main)
eventloop.run()