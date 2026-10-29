
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class SamiCyberHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "ok",
                "message": "Sami Cyber server is running"
            }).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print("Request received")

server = HTTPServer(("0.0.0.0", 10000), SamiCyberHandler)
print("Sami Cyber server started on port 10000")
server.serve_forever()

