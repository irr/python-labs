import sys
sys.path.append("/usr/lib/python2.7/site-packages")

from concurrence import dispatch
from concurrence.web import Application, Controller, web

class TestController(Controller):

    @web.route('/hello')
    def hello(self):
        return "Hello World!"
    
    @web.route('/pipe')
    def pipe(self):
        with open('/tmp/workfile', 'r') as f:
            f.read()
        f.close()
        return "OK"
    
if __name__ == '__main__':    
    application = Application()
    application.add_controller(TestController())
    application.configure()
    server = application.serve(('localhost', 8080))
    dispatch(server)    