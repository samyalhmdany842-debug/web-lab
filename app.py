
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

PAGE = """<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CYBER LAB | مختبر الأمن السيبراني</title>
<style>
* { box-sizing: border-box; }
body {
  margin: 0; padding: 20px;
  background: #050807; color: #62ff9b;
  font-family: Consolas, monospace;
}
main { max-width: 850px; margin: auto; }
header, section {
  border: 1px solid #17683b;
  background: #09130e;
  padding: 18px; margin-bottom: 16px;
  border-radius: 8px;
}
h1 { font-size: 26px; text-shadow: 0 0 12px #1aff77; }
h2 { font-size: 18px; }
p { color: #b7f7ce; }
.status { color: #62ff9b; font-weight: bold; }
button {
  background: #103d25; color: #7dffad;
  border: 1px solid #36d879; border-radius: 5px;
  padding: 11px 15px; margin: 5px; cursor: pointer;
}
button:hover { background: #1b6139; }
#log {
  background: #020403; border: 1px solid #194b2e;
  padding: 12px; min-height: 65px;
  white-space: pre-wrap; overflow-wrap: anywhere;
}
video {
  width: 100%; max-width: 420px;
  display: block; margin: 15px auto;
  border: 1px solid #36d879; border-radius: 6px;
}
.small { font-size: 12px; color: #80b997; }
</style>
</head>
<body>
<main>
<header>
  <p class="small">CYBER LAB / EDUCATIONAL MONITOR</p>
  <h1>مختبر الأمن السيبراني</h1>
  <p>لوحة مراقبة تعليمية بسيطة</p>
  <p>حالة الخادم: <span class="status" id="status">لم يتم الفحص</span></p>
</header>

<section>
  <h2>[ 01 ] فحص الخادم</h2>
  <p>اضغط الزر للتحقق من استجابة الخادم.</p>
  <button onclick="checkServer()">فحص الخادم</button>
  <h2>سجل الفحص</h2>
  <div id="log">بانتظار بدء الفحص...</div>
</section>

<section>
  <h2>[ 02 ] اختبار الكاميرا</h2>
  <p>تعمل الكاميرا فقط بعد ضغطك على التشغيل والسماح للمتصفح.</p>
  <button onclick="startCamera()">تشغيل الكاميرا</button>
  <button onclick="stopCamera()">إيقاف الكاميرا</button>
  <p id="cameraResult">الكاميرا متوقفة.</p>
  <video id="camera" autoplay playsinline muted></video>
</section>

<footer class="small">
  CYBER LAB — تجربة تعليمية. لا تُرسل معاينة الكاميرا إلى الخادم.
</footer>
</main>

<script>
function addLog(message) {
  const log = document.getElementById('log');
  const time = new Date().toLocaleTimeString();
  log.textContent = '[' + time + '] ' + message + '\\n' + log.textContent;
}

async function checkServer() {
  document.getElementById('status').textContent = 'جارٍ الفحص...';
  try {
    const response = await fetch('/status', {method: 'POST'});
    const message = await response.text();
    if (!response.ok) throw new Error('HTTP ' + response.status);
    document.getElementById('status').textContent = 'ONLINE';
    addLog('نجح الفحص: ' + message);
  } catch (error) {
    document.getElementById('status').textContent = 'OFFLINE';
    addLog('فشل الاتصال بالخادم.');
  }
}

let cameraStream = null;
async function startCamera() {
  try {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      throw new Error('camera unavailable');
    }
    cameraStream = await navigator.mediaDevices.getUserMedia({video: true});
    document.getElementById('camera').srcObject = cameraStream;
    document.getElementById('cameraResult').textContent = 'الكاميرا تعمل على جهازك فقط.';
    addLog
  } catch (error) {
    document.getElementById('cameraResult').textContent = 'لم تعمل الكاميرا. تحقق من إذن المتصفح.';
    addLog('تعذر تشغيل الكاميرا.');
  }
}

function stopCamera() {
  if (cameraStream) {
    cameraStream.getTracks().forEach(track => track.stop());
    cameraStream = null;
  }
  document.getElementById('camera').srcObject = null;
  document.getElementById('cameraResult').textContent = 'تم إيقاف الكاميرا.';
  addLog('تم إيقاف الكاميرا.');
}
</script>
</body>
</html>""".encode("utf-8")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(PAGE)))
            self.end_headers()
            self.wfile.write(PAGE)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/status":
            body = "الخادم يعمل بنجاح.".encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)

port = int(os.environ.get("PORT", "8000"))
HTTPServer(("0.0.0.0", port), Handler).serve_forever()
