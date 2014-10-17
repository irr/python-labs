import falcon

class WebResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = ('Test OK!')

# falcon.API instances are callable WSGI apps
app = falcon.API()

# Resources are represented by long-lived class instances
web = WebResource()

# things will handle all requests to the '/' URL path
app.add_route('/', web)

# gunicorn -w 4 -k eventlet --threads 100 --worker-connections 100 -b localhost:1972 --log-level info --error-logfile - --log-file - --access-logfile - web:app