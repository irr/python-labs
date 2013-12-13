from bottle import route, run, request, response
import json

@route('/', method='GET')
def do_form():
    meta = { 'id':1, 'name':'test.png' }
    form = """
          <!doctype html>
          <html lang="en">
          <head>
            <meta charset="utf-8">
            <title>Upload Test</title>
          </head>
          <body>
          <form action="/upload" method="post" 
                enctype="multipart/form-data">
            <textarea name=meta rows=10 cols=60>%s</textarea><br/>
            <input type="file" name="data"/>
            <input type="submit" value="POST data" />
          </form>
          </body>
          </html>
    """ % (json.dumps(meta),)
    response.content_type = 'text/html; charset=utf-8'
    return form

@route('/upload', method='POST')
def do_upload():
    meta = request.forms.meta
    data = request.files.get("data")
    if data and data.file:
        raw = data.file.read()
        filename = data.filename
        data.save("/tmp/%s" % filename, overwrite=True, chunk_size=65536)
        return "<b>Metadata:</b><br/>%s<hr/>You uploaded <b>%s</b> (<b>%d</b> bytes)." \
                % (meta, filename, len(raw))
    return "You missed a field."

run(host='0.0.0.0', port=8080, debug=True, reloader=True)
