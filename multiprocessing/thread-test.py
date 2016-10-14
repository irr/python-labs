from threading import Thread

#defining a global variable
mylist = []

def somefunc(a):
    global mylist
    mylist.append(a)
    print("somefunc: {0}".format(mylist))

def main():
    for i in range(10):
       t = Thread(target=somefunc,args=(i,))
       t.start()
    t.join()

main()
print(mylist)
