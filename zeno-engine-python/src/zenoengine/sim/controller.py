from __future__ import annotations
from zenoengine.config.config import PGNSConfig
from zenoengine.sim.pgns_sim import PGNSSimulation
from zenoengine.sim.classical_sim import ClassicalSimulation

def run_simulation(config: PGNSConfig) -> None:
    if config.mode == "symbolic":
        print(f"[PGNSSimulation] Starting simulation in mode: symbolic")
        sim = PGNSSimulation(config)
    elif config.mode == "classical":
        print(f"[ClassicalSimulation] Starting simulation in mode: classical")
        sim = ClassicalSimulation(config)
    else:
        raise ValueError(f"Unknown simulation mode: {config.mode}")

    sim.run()
