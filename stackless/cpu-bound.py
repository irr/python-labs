import stackless

# http://entitycrisis.blogspot.com.br/2009/06/stackless-vs-gil-its-draw.html

#A contrived CPU bound task
def factorial(c):
    T = 1 
    for i in xrange(1, c):
        T *= i
    print("number length: %d" % len(str(T)))
    return T

#create two tasklets
stackless.tasklet(factorial)(1024)
stackless.tasklet(factorial)(2048)

#used to track of how many task switches happen
switches = {}

#while there is more than the main task running...
while stackless.getruncount() > 1:
    #run the schedule for 100 ticks
    task = stackless.run(100)
    #if we have a pre-empted task
    if task:
        #increment it's switch counter
        C = switches.setdefault(task, 0)
        switches[task] += 1
        #insert it at the end of the schedule
        task.insert()

print("switches     : %s" % switches.values())
