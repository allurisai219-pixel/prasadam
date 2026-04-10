---

title: prasadam-flow
sdk: docker
---

# Prasadam-Flow OpenEnv

## Overview

Prasadam-Flow is a reinforcement learning environment that simulates a large-scale temple kitchen serving thousands of pilgrims.

The system models:

* Cooking delays (inertia)
* Food spoilage (perishability)
* Dynamic demand patterns

The goal is to maximize food distribution efficiency while minimizing waste.

---

## Environment

* 24 time steps (1 day)
* Multiple cooking vats
* Food freshness decay over time
* Resource constraints (fuel and supply)

---

## Actions

* START_SMALL_BATCH
* START_LARGE_BATCH
* HOLD

---

## Tasks

* Task 1: Stable demand
* Task 2: Random surges
* Task 3: High volatility with constraints

---

## API

The application exposes a simple HTTP API:

* GET `/` → health check
* POST `/reset` → reset environment
* POST `/step` → step environment

---

## Run

The application runs via Docker and starts a server on port 7860.
