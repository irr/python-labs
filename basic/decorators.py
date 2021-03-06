from functools import wraps

class wrapperClass(object):
    def __init__(self, f):
        print "\ninside wrapperClass.__init__(): %s" % f
        self.f = f

    def __call__(self, *args):
        print "begin wrapperClass.__call__(): %s" % self.f
        self.f(*args)
        print "end wrapperClass.__call__(): %s\n" % self.f

@wrapperClass
def func1(*args):
    print "inside func1()[%s](%d)" % (args, len(args))

print "finished decorating func1() and ready to call it!\n"

def wrapperFunc(f):
    @wraps(f)
    def new_f(*args):
        print "entering %s: %s" % (f.__name__, f)
        f(*args)
        print "exited %s: %s\n" % (f.__name__, f)
    return new_f

@wrapperFunc
def func2(*args):
    print "inside func2()[%s](%d)" % (args, len(args))


print "wrapperClass:"
func1(1, "2", {"x":3})

print "wrapperFunc:"
func2(4, "5", 6, {"y":7, "z":8})

# OUTPUT:
# inside wrapperClass.__init__(): <function func1 at 0x7f...7fdc9b0>
# finished decorating func1() and ready to call it!

# wrapperClass:
# begin wrapperClass.__call__(): <function func1 at 0x7f...7fdc9b0>
# inside func1()[(1, '2', {'x': 3})](3)
# end wrapperClass.__call__(): <function func1 at 0x7f...7fdc9b0>

# wrapperFunc:
# entering func2: <function func2 at 0x7f...7fdcb90>
# inside func2()[(4, '5', 6, {'y': 7, 'z': 8})](4)
# exited func2: <function func2 at 0x7f...7fdcb90>

from itertools import chain
def foo(a,b,c,d):
        print a,b,c,d

print "itertools(chain):"
tup1 = (1,2)
tup2 = (3,4)
print "using tuples..."
foo(*chain(tup1,tup2))

print "using lists..."
foo(*chain(list(tup1),list(tup2)))

from functools import partial
goo = partial(partial(partial(foo, 11), 22), 33)
print "\nitertools(partial,aka curry):"
print "foo:%s\ngoo:%s" % (foo,goo)
goo(44)