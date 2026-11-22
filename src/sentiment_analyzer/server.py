"""Small web server: shows the page and runs the analyzer when the page asks.

Run `python -m sentiment_analyzer.server` and open http://localhost:8000.

    GET  /api/report    analyze the dataset in data/ and return the report
    POST /api/classify  classify one review (not saved)
    POST /api/add       add one review to the dataset and return the new report
"""

import json
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from . import analyzer

PORT = 8000
HOST = os.environ.get("HOST", "127.0.0.1")  # Docker sets HOST=0.0.0.0


class Handler(SimpleHTTPRequestHandler):
    """Files from web/ plus the three /api/ routes above."""

    def do_GET(self):
        if self.path == "/api/report":
            self.send_json(analyzer.analyze(analyzer.DATASET))
        else:
            super().do_GET()  # index.html, app.js, styles.css...

    def do_POST(self):
        try:
            size = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(size))
            if self.path == "/api/classify":
                self.send_json(analyzer.classify_text(body["text"]))
            elif self.path == "/api/add":
                analyzer.add_review(body["text"], body.get("product", ""), analyzer.DATASET)
                self.send_json(analyzer.analyze(analyzer.DATASET))
            else:
                self.send_json({"error": "Not found"}, status=404)
        except (ValueError, KeyError, TypeError) as error:
            self.send_json({"error": str(error)}, status=400)  # bad input
        except Exception as error:
            self.send_json({"error": f"Something failed: {error}"}, status=500)

    def do_OPTIONS(self):
        """The browser asks first if the GitHub Pages site may call this server."""
        self.send_response(204)
        self.allow_other_sites()
        self.end_headers()

    def allow_other_sites(self):
        """CORS: let the page on GitHub Pages talk to this server on my PC."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Private-Network", "true")

    def send_json(self, data: dict, status: int = 200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.allow_other_sites()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class Server(ThreadingHTTPServer):
    # On Windows this option lets two servers share port 8000 by mistake; turn it off there.
    allow_reuse_address = os.name != "nt"


def make_server(port: int = PORT) -> Server:
    handler = partial(Handler, directory=str(analyzer.PROJECT / "web"))
    return Server((HOST, port), handler)


if __name__ == "__main__":
    try:
        httpd = make_server()
    except OSError:
        raise SystemExit(f"Port {PORT} is busy: the server is already running in another window.")
    print(f"Open http://localhost:{PORT} or the GitHub Pages link  (Ctrl+C to stop)")
    httpd.serve_forever()
