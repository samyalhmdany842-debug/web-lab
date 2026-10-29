
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import json
import os
import threading
import time

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
BASE_URL = "https://sami-cyber-api-2.onrender.com"

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Camera Permission</title>
<style>
body {
  font-family: Arial, sans-serif;
  max-width: 420px;
  margin: 70px auto;
  padding: 20px;
  text-align: center;
}
button {
  padding: 12px 24px;
  margin: 8px;
  cursor: pointer;
}
video { width: 100%; margin-top: 18px; }
</style>
</head>
<body>
<h2>Allow Camera Access?</h2>
<p>This website is requesting permission to use your camera.
No photo will be taken or sent without your confirmation.</p>
<button id="allow">Allow</button>
<button id="deny">Deny</button>
<p id="status"></p>
<video id="video" autoplay playsinline hidden></video>
<script>
const status = document.getElementById("status");
const video = document.getElementById("video");
let stream;

document.getElementById("allow").onclick = async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({video: true});
    video.srcObject = stream;
    video.hidden = false;
    status.textContent =
      "Camera is on. No photo has been taken or sent.";
  } catch (e) {
    status.textContent =
      "Camera access was not granted. Check your browser permission.";
  }
};

document.getElementById("deny").onclick = () => {
  if (stream) stream.getTracks().forEach(track => track.stop());
  video.hidden = true;
  status.textContent = "Camera access denied.";
};
</script>
</body>
</html>"""


def telegram_call(method, data):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    payload = json.dumps(data).encode("utf-8")
    request = Request(
        url, data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urlopen(request, timeout=35) as response:
        return json.loads(response.read().decode("utf-8"))


def bot_loop():
    offset = 0
    while True:
        try:
            result = telegram_call("getUpdates", {
                "offset": offset,
                "timeout": 25,
                "allowed_updates": ["message"]
            })
            for update in result.get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message", {})
                chat = message.get("chat", {}).get("id")
                text = message.get("text", "")
                if chat and text.split("@")[0] == "/start":
                    telegram_call("sendMessage", {
                        "chat_id": chat,
                        "text": (
                            "Welcome to Sami Cyber!\\n"
                            f"Open the camera page: {BASE_URL}/camera\\n"
                            "The page asks for camera permission."
                        )
                    })
        except Exception as error:
            print("Telegram bot error:", error)
            time.sleep(5)


class SamiCyberHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?", 1)[0]

        if path == "/camera":
            body = PAGE.encode("utf-8")
            content_type = "text/html; charset=utf-8"
            status = 200
        elif path == "/health":
            body = json.dumps({
                "status": "ok",
                "message": "Sami Cyber server is running"
            }).encode("utf-8")
            content_type = "application/json; charset=utf-8"
            status = 200
        elif path == "/":
            body = b"Sami Cyber server is running"
            content_type = "text/plain; charset=utf-8"
            status = 200
        else:
            body = b'{"status":"error","message":"Page not found"}'
            content_type = "application/json; charset=utf-8"
            status = 404

        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        print(format % args)


port = int(os.environ.get("PORT", "10000"))

if TOKEN:
    threading.Thread(target=bot_loop, daemon=True).start()
else:
    print("TELEGRAM_BOT_TOKEN is missing in Environment")

server = ThreadingHTTPServer(("0.0.0.0", port), SamiCyberHandler)
print(f"Sami Cyber server started on port {port}")
server.serve_forever()
