import random
from typing import Tuple, Dict, Any

from models import VatState, ObservationSpace, Action


class TempleKitchenEnv:
    def __init__(self, task_level: int = 1):
        self.task_level = task_level
        self.max_steps = 24
        self.num_vats = 5
        self.reset()

    def reset(self) -> ObservationSpace:
        self.hour = 0
        self.done = False

        self.pilgrims = random.randint(20000, 50000)
        self.fuel = 100.0 if self.task_level != 3 else 60.0
        self.supply = 100.0

        self.vats = [
            VatState(0, 0.0, 1.0, False, False)
            for _ in range(self.num_vats)
        ]

        self.stats = {"fed": 0, "waste": 0, "unmet": 0}

        return self._get_obs()

    def state(self) -> ObservationSpace:
        return self._get_obs()

    def _get_obs(self) -> ObservationSpace:
        return ObservationSpace(
            pilgrim_count=self.pilgrims,
            vats=self.vats,
            fuel_remaining=self.fuel,
            supply_remaining=self.supply,
            hour=self.hour,
        )

    def step(self, action: Action) -> Tuple[ObservationSpace, float, bool, Dict[str, Any]]:
        if self.done:
            return self._get_obs(), 0.0, True, {}

        reward = 0.0

        if action == Action.START_SMALL_BATCH:
            self._start_batch("small")
        elif action == Action.START_LARGE_BATCH:
            self._start_batch("large")

        total_food = 0.0

        for vat in self.vats:
            if vat.is_cooking:
                vat.cook_timer -= 1
                if vat.cook_timer <= 0:
                    vat.is_cooking = False
                    vat.is_ready = True
                    vat.freshness = 1.0

            if vat.is_ready:
                vat.freshness -= 0.15

                if vat.freshness < 0.2:
                    self.stats["waste"] += vat.quantity
                    vat.quantity = 0.0
                    vat.is_ready = False
                else:
                    total_food += vat.quantity * vat.freshness

        demand = self._get_demand()

        fed = min(total_food, demand)
        unmet = max(0, demand - fed)

        self.stats["fed"] += fed
        self.stats["unmet"] += unmet

        reward += fed * 0.001
        reward -= unmet * 0.002
        reward -= self.stats["waste"] * 0.001

        if self.hour == self.max_steps - 1:
            waste_rate = self.stats["waste"] / (self.stats["fed"] + self.stats["waste"] + 1e-6)
            if waste_rate < 0.05:
                reward += 5.0

        self.hour += 1
        self._drift_system()

        self.done = self.hour >= self.max_steps

        return self._get_obs(), reward, self.done, {
            "fed": fed,
            "unmet": unmet,
            "waste": self.stats["waste"]
        }

    def _start_batch(self, size: str):
        if self.supply <= 0:
            return

        for vat in self.vats:
            if not vat.is_cooking and not vat.is_ready:
                vat.is_cooking = True
                vat.cook_timer = 3 if size == "small" else 5
                vat.quantity = 100.0 if size == "small" else 200.0

                self.supply -= 2 if size == "small" else 4
                self.fuel -= 1
                break

    def _get_demand(self) -> float:
        base = 30000

        if self.task_level == 1:
            return base

        if self.task_level == 2:
            return base * 3 if random.random() < 0.2 else base

        return base * random.choice([1, 2, 5])

    def _drift_system(self):
        if self.task_level == 3:
            self.fuel -= random.uniform(0.5, 2.0)
        else:
            self.fuel -= 0.5


class Task1Env(TempleKitchenEnv):
    def __init__(self):
        super().__init__(1)

    def agent_grader(self, stats):
        return min(1.0, stats["fed"] / (stats["fed"] + stats["unmet"] + 1e-6))


class Task2Env(TempleKitchenEnv):
    def __init__(self):
        super().__init__(2)

    def agent_grader(self, stats):
        efficiency = stats["fed"] / (stats["fed"] + stats["unmet"] + 1e-6)
        waste_penalty = stats["waste"] / 50000
        return max(0.0, min(1.0, efficiency - waste_penalty))


class Task3Env(TempleKitchenEnv):
    def __init__(self):
        super().__init__(3)

    def agent_grader(self, stats):
        efficiency = stats["fed"] / (stats["fed"] + stats["unmet"] + 1e-6)
        waste_penalty = stats["waste"] / 30000
        fuel_penalty = max(0, 1 - self.fuel / 60)
        return max(0.0, min(1.0, efficiency - waste_penalty - fuel_penalty))