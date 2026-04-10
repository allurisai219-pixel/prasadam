from dataclasses import dataclass
from enum import Enum
from typing import List


class Action(Enum):
    START_SMALL_BATCH = 0
    START_LARGE_BATCH = 1
    HOLD = 2


@dataclass
class VatState:
    """
    Represents a Mega-Vat in the temple kitchen.
    """
    cook_timer: int
    quantity: float
    freshness: float
    is_cooking: bool
    is_ready: bool


@dataclass
class ObservationSpace:
    """
    Full environment observation returned to the agent.
    """
    pilgrim_count: int
    vats: List[VatState]
    fuel_remaining: float
    supply_remaining: float
    hour: int