# 🍛 Prasadam-Flow OpenEnv

## Overview

Prasadam-Flow models a large-scale temple kitchen serving 50,000+ pilgrims daily. The system introduces two core RL challenges:

- **Stochastic Demand Modeling** (hourly pilgrim fluctuations)
- **Inertia-Aware Action Planning** (delayed cooking activation)
- **Perishability-Constrained Inventory Control**
- **Dense Reward Shaping under Waste Minimization Objectives**

---

## Environment Dynamics

Each episode spans **24 hours (24 steps)**.

### Key Mechanisms

#### 1. Inertia (Lead-Time Delay)
- Small batch: 3-step cook time
- Large batch: 5-step cook time
- Food is not immediately usable after action

#### 2. Perishability
- Freshness starts at 1.0 when ready
- Degrades by 0.15 per step
- Below 0.2 → food becomes waste

---

## Observation Space

```python
ObservationSpace(
    pilgrim_count: int,
    vats: List[VatState],
    fuel_remaining: float,
    supply_remaining: float,
    hour: int
)