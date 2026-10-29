

import os
from http.server import BaseHTTPRequestHandler, HTTPServer

PAGE = """<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>مختبر الوظائف</title>
</head>
<body>
<h1>مختبر الوظائف</h1>
<p>اضغط الزر لفحص الخادم.</p>
<button onclick="checkServer()">افحص الخادم</button>
<p id="result">لم يُجرَ الفحص بعد.</p>
<script>
async function checkServer() {
  const response = await fetch('/status', {method: 'POST'});
  const result = await response.text();
  document.getElementById('result').textContent = result;
}
</script>
</body>
</html>""".encode("utf-8")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            body = PAGE
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/status':
            body = 'الخادم يعمل بنجاح.'.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)

port = int(os.environ.get("PORT", "8000"))
HTTPServer(("0.0.0.0", port), Handler).serve_forever()
