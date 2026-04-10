from models import Action
from environment import Task1Env, Task2Env, Task3Env
import time


def run():
    print("🚀 Prasadam Flow started")

    envs = [Task1Env(), Task2Env(), Task3Env()]

    for i, env in enumerate(envs):
        print(f"\nRunning Task {i+1}...")

        obs = env.reset()
        done = False

        while not done:
            obs, reward, done, info = env.step(Action.HOLD)

        score = env.agent_grader(env.stats)
        print(f"Task {i+1} Score: {score}")

    print("\n✅ All tasks completed")

    # 🔥 KEEP APP ALIVE (IMPORTANT)
    while True:
        time.sleep(60)


if __name__ == "__main__":
    run()
