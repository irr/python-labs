from app import microweb


@microweb.route('/')
@microweb.route('/index')
def index():
    return "Hello, World!"
