import stackless
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-n", type="int", dest="num_tasklets", help="how many", default=100000)

def f(left, right):
    left.send(right.receive()+1)

def main():
    options, args = parser.parse_args()
    leftmost = stackless.channel()
    left, right = None, leftmost
    for i in xrange(options.num_tasklets):
        left, right = right, stackless.channel()
        stackless.tasklet(f)(left, right)
    right.send(0)
    x = leftmost.receive()
    print x

stackless.tasklet(main)()
stackless.run()
