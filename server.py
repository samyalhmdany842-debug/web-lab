
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

class SamiCyberHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            body = json.dumps({
                "status": "ok",
                "message": "Sami Cyber server is running"
            }).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        elif self.path == "/":
            body = b"Sami Cyber server is running"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print(format % args)

port = int(os.environ.get("PORT", "10000"))
server = HTTPServer(("0.0.0.0", port), SamiCyberHandler)
print(f"Sami Cyber server started on port {port}")
server.serve_forever()



 


