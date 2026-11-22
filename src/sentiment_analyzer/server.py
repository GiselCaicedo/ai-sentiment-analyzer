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

    def send_json(self, data: dict, status: int = 200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def make_server(port: int = PORT) -> ThreadingHTTPServer:
    handler = partial(Handler, directory=str(analyzer.PROJECT / "web"))
    return ThreadingHTTPServer((HOST, port), handler)


if __name__ == "__main__":
    print(f"Open http://localhost:{PORT}  (Ctrl+C to stop)")
    make_server().serve_forever()
