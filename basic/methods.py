class A(object):
    def foo(self, x):
        print "executing foo(%s,%s)" % (self, x)

    @classmethod
    def class_foo(cls, x):
        print "executing class_foo(%s,%s)" % (cls, x)

    @staticmethod
    def static_foo(x):
        print "executing static_foo(%s)" % (x,)    

a = A()
a.foo(10)
A.class_foo(100)
A.static_foo(1000)

print(a.foo)
print(A.class_foo)
print(A.static_foo)