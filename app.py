import time
from models import Action
from environment import Task1Env, Task2Env, Task3Env


def run():
    print("🚀 Prasadam Flow App Started")

    envs = [Task1Env(), Task2Env(), Task3Env()]

    for i, env in enumerate(envs):
        print(f"Running Task {i+1}...")

        obs = env.reset()
        done = False

        while not done:
            obs, reward, done, info = env.step(Action.HOLD)

        score = env.agent_grader(env.stats)
        print(f"Task {i+1} Score: {score}")

    print("✅ Finished all tasks")

# Run once
try:
    run()
except Exception as e:
    print("ERROR:", str(e))

# 🔥 KEEP CONTAINER ALIVE FOREVER
while True:
    time.sleep(60)
