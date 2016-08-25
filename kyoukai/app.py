import json
from kyoukai import Kyoukai, HTTPRequestContext

kyk = Kyoukai("example_app")

@kyk.route("/", methods=["GET", "POST"])
async def index(ctx: HTTPRequestContext):
    return json.dumps(list(ctx.request.headers.items())), 200, {"Content-Type": "application/json"}

kyk.run()
