from models import Action
from environment import Task1Env, Task2Env, Task3Env


class HeuristicAgent:
    """
    Simple baseline agent for Prasadam-Flow.

    Strategy:
    - If demand likely high → start large batch
    - Otherwise → start small batch
    - Occasionally HOLD to avoid overproduction (waste control)
    """

    def __init__(self):
        self.step_count = 0

    def act(self, obs):
        self.step_count += 1

        # Simple heuristic: cycle behavior
        if self.step_count % 6 == 0:
            return Action.HOLD

        # crude demand intuition from pilgrim count
        if obs.pilgrim_count > 35000:
            return Action.START_LARGE_BATCH

        if obs.pilgrim_count > 25000:
            return Action.START_SMALL_BATCH

        return Action.HOLD


def run_episode(env, agent, max_steps=24):
    obs = env.reset()
    total_reward = 0.0
    done = False

    while not done:
        action = agent.act(obs)
        obs, reward, done, info = env.step(action)
        total_reward += reward

    score = env.agent_grader(env.stats)

    return total_reward, score


def main():
    print("\n🍛 Prasadam-Flow Inference Run Starting...\n")

    envs = [
        ("Task 1 (Easy)", Task1Env()),
        ("Task 2 (Medium)", Task2Env()),
        ("Task 3 (Hard)", Task3Env()),
    ]

    agent = HeuristicAgent()

    results = []

    for name, env in envs:
        print(f"Running {name}...")
        total_reward, score = run_episode(env, agent)

        results.append((name, total_reward, score))

        print(f"  Total Reward: {total_reward:.2f}")
        print(f"  Grader Score: {score:.4f}\n")

    print("========== FINAL RESULTS ==========")
    for name, reward, score in results:
        print(f"{name}: Reward={reward:.2f} | Score={score:.4f}")

    print("\n✅ Inference completed successfully.")


if __name__ == "__main__":
    main()