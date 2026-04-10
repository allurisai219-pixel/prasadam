import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models import Action
from environment import Task1Env


env = Task1Env()


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            data = json.loads(body.decode())
        except:
            data = {}

        if self.path == "/reset":
            obs = env.reset()
            response = {"hour": obs.hour}

        elif self.path == "/step":
            action = data.get("action", "HOLD")
            try:
                action = Action[action]
            except:
                action = Action.HOLD

            obs, reward, done, info = env.step(action)

            response = {
                "reward": reward,
                "done": done
            }

        else:
            response = {"error": "invalid endpoint"}

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())


def main():
    print("🚀 Server started on port 7860", flush=True)
    server = HTTPServer(("0.0.0.0", 7860), Handler)
    server.serve_forever()


# 🔥 IMPORTANT: this line
if __name__ == "__main__":
    main()
