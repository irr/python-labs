import flask
import requests

# pip install opentelemetry-api
# pip install opentelemetry-sdk
# pip install opentelemetry-instrumentation-flask
# pip install opentelemetry-instrumentation-requests

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)

trace.set_tracer_provider(TracerProvider())
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)

app = flask.Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

tracer = trace.get_tracer(__name__)

@app.route("/")
def hello():
    with tracer.start_as_current_span("example-request"):
        requests.get("https://www.google.com")
    return "hello"


app.run(port=5000)
