from bottle import route, run, request, response

@route('/', method='GET')
def do_form():
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
  <input type="file" name="data" />
  <input type="submit" value="Send" />
</form>
</body>
</html>
    """
    response.content_type = 'text/html; charset=utf-8'
    return form


@route('/upload', method='POST')
def do_upload():
    data = request.files.get("data")
    if data and data.file:
        raw = data.file.read()
        filename = data.filename
        # 0.12 - data.save("/tmp/%s" % filename)
        with open("/tmp/%s" % filename, 'w+') as open_file:
            open_file.write(raw)
        return "You uploaded %s (%d bytes)." % (filename, len(raw))

    return "You missed a field."

run(host='localhost', port=8080, debug=True, reloader=True)
