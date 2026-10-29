import os
from http.server import BaseHTTPRequestHandler, HTTPServer

PAGE = """<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>مختبر الوظائف</title>
<style>
body { font-family: sans-serif; text-align: center; padding: 24px; }
button { padding: 12px 18px; margin: 8px; }
video { width: 100%; max-width: 420px; margin-top: 16px; }
</style>
</head>
<body>
<h1>مختبر الوظائف</h1>
<button onclick="checkServer()">افحص الخادم</button>
<p id="result">اضغط لفحص الخادم.</p>

<h2>اختبار الكاميرا</h2>
<p>اضغط تشغيل الكاميرا واسمح للمتصفح باستخدامها إذا رغبت.</p>
<button onclick="startCamera()">تشغيل الكاميرا</button>
<button onclick="stopCamera()">إيقاف الكاميرا</button>
<p id="cameraResult"></p>
<video id="camera" autoplay playsinline muted></video>

<script>
async function checkServer() {
  const response = await fetch('/status', {method: 'POST'});
  document.getElementById('result').textContent = await response.text();
}
let cameraStream = null;
async function startCamera() {
  try {
    cameraStream = await navigator.mediaDevices.getUserMedia({video: true});
    document.getElementById('camera').srcObject = cameraStream;
    document.getElementById('cameraResult').textContent = 'الكاميرا تعمل على جهازك فقط.';
  } catch (error) {
    document.getElementById('cameraResult').textContent = 'لم يتم تشغيل الكاميرا. تحقق من الإذن.';
  }
}
function stopCamera() {
  if (cameraStream) {
    cameraStream.getTracks().forEach(track => track.stop());
    cameraStream = null;
  }
  document.getElementById('camera').srcObject = null;
  document.getElementById('cameraResult').textContent = 'تم إيقاف الكاميرا.';
}
</script>
</body>
</html>""".encode("utf-8")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(PAGE)))
            self.end_headers()
            self.wfile.write(PAGE)
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
