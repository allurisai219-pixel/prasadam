import time
import sys

print("🔥 APP STARTED", flush=True)

try:
    from models import Action
    from environment import Task1Env, Task2Env, Task3Env

    print("✅ Imports successful", flush=True)

    envs = [Task1Env(), Task2Env(), Task3Env()]

    for i, env in enumerate(envs):
        print(f"🚀 Running Task {i+1}", flush=True)

        obs = env.reset()
        done = False

        while not done:
            obs, reward, done, info = env.step(Action.HOLD)

        score = env.agent_grader(env.stats)
        print(f"✅ Task {i+1} Score: {score}", flush=True)

    print("🎉 All tasks completed", flush=True)

except Exception as e:
    print("❌ ERROR OCCURRED:", str(e), flush=True)
    import traceback
    traceback.print_exc()

# KEEP ALIVE (VERY IMPORTANT)
while True:
    print("⏳ Alive...", flush=True)
    time.sleep(30)
