import time
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading

from models import Action
from environment import Task1Env, Task2Env, Task3Env


def run_env():
    print("🚀 Prasadam Flow Started", flush=True)

    envs = [Task1Env(), Task2Env(), Task3Env()]

    for i, env in enumerate(envs):
        print(f"Running Task {i+1}", flush=True)

        obs = env.reset()
        done = False

        while not done:
            obs, reward, done, info = env.step(Action.HOLD)

        score = env.agent_grader(env.stats)
        print(f"Task {i+1} Score: {score}", flush=True)

    print("✅ All tasks done", flush=True)


# 🔥 SIMPLE WEB SERVER FOR HF
def start_server():
    server = HTTPServer(("0.0.0.0", 7860), SimpleHTTPRequestHandler)
    print("🌐 Server running on port 7860", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    # Run env in background
    threading.Thread(target=run_env).start()

    # Start web server (THIS FIXES HF)
    start_server()
