from multiprocessing import Process

#defining a global variable
mylist = []

def somefunc(a):
    global mylist
    mylist.append(a)
    print("somefunc:", mylist)

def main():
    for i in range(10):
       t = Process(target=somefunc,args=(i,))
       t.start()
    t.join()

main()
print(mylist)