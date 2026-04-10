import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from models import Action
from environment import Task1Env, Task2Env, Task3Env

envs = {
    "task1": Task1Env(),
    "task2": Task2Env(),
    "task3": Task3Env(),
}


class Handler(BaseHTTPRequestHandler):
    def _send(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        self._send({"status": "running"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            data = json.loads(body.decode())
        except:
            data = {}

        task = data.get("task", "task1")
        env = envs.get(task, envs["task1"])

        if self.path == "/reset":
            obs = env.reset()
            self._send({"hour": obs.hour})

        elif self.path == "/step":
            action = data.get("action", "HOLD")
            try:
                action = Action[action]
            except:
                action = Action.HOLD

            obs, reward, done, info = env.step(action)
            self._send({
                "reward": reward,
                "done": done,
                "info": info
            })

        else:
            self._send({"error": "invalid endpoint"})


def main():
    server = HTTPServer(("0.0.0.0", 7860), Handler)
    print("Server running on 7860", flush=True)
    server.serve_forever()
