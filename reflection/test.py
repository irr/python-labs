import sys

class W:
    def pA(self):
        print "inside pA [{0}]".format(id(self))
    def pB(self):
        print "inside pB [{0}]".format(id(self))

w = getattr(sys.modules[__name__], "W")()
print w, id(w)

methods = [m for m in dir(w.__class__) if not m.startswith('_')]

for m in methods:
    getattr(w, m)()

