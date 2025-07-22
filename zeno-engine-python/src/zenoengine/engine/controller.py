from __future__ import annotations

from from zenocore.config.types import ZenoConfig
from zenoengine.engine.base import BaseSimulation
from zenoengine.engine.pgns_sim import PGNSSimulation
from zenoengine.engine.classical_sim import ClassicalSimulation
from zenoengine.engine.rehte.sim import REHTESimulation


def run_simulation(config: ZenoConfig) -> None:
    sim_class = resolve_simulation(config)
    sim = sim_class(config)
    sim.run()


def resolve_simulation(config: ZenoConfig) -> type[BaseSimulation]:
    operator = config.defaults.operator.lower()
    mode = config.defaults.mode.lower()

    if operator == "pgns" and mode == "symbolic":
        return PGNSSimulation
    elif operator == "rehte" and mode == "symbolic":
        return REHTESimulation
    elif mode == "classical":
        return ClassicalSimulation
    else:
        raise ValueError(f"Unsupported simulation mode/operator: mode={mode}, operator={operator}")
