import json
from http.server import BaseHTTPRequestHandler, HTTPServer

from models import Action
from environment import Task1Env, Task2Env, Task3Env

# Initialize environments
envs = {
    "task1": Task1Env(),
    "task2": Task2Env(),
    "task3": Task3Env(),
}


class Handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        response = {
            "message": "Prasadam Flow API is running",
            "endpoints": ["/reset", "/step", "/health"]
        }
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body.decode("utf-8"))
        except:
            data = {}

        task = data.get("task", "task1")
        env = envs.get(task, envs["task1"])

        if self.path == "/reset":
            obs = env.reset()
            response = {
                "status": "reset",
                "task": task,
                "hour": obs.hour,
                "pilgrims": obs.pilgrim_count
            }

        elif self.path == "/step":
            action_str = data.get("action", "HOLD")

            try:
                action = Action[action_str]
            except:
                action = Action.HOLD

            obs, reward, done, info = env.step(action)

            response = {
                "reward": reward,
                "done": done,
                "info": info,
                "hour": obs.hour,
                "pilgrims": obs.pilgrim_count
            }

        elif self.path == "/health":
            response = {"status": "ok"}

        else:
            response = {"error": "Invalid endpoint"}

        self._set_headers()
        self.wfile.write(json.dumps(response).encode())


def run_server():
    server_address = ("0.0.0.0", 7860)
    httpd = HTTPServer(server_address, Handler)
    print("🌐 Prasadam Flow server running on port 7860", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
