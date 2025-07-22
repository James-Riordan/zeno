from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from zenoengine.io.export import export_snapshot

if TYPE_CHECKING:
    from from zenocore.config.types import ZenoConfig
    from zenoengine.fields.field import SymbolicField


class BaseSimulation(ABC):
    """
    Abstract base class for all Zeno simulations.
    Handles common simulation logic (field, timing, steps, config).
    Subclasses must implement `step()` and optionally override `run()`.
    """

    def __init__(self, config: ZenoConfig):
        self.config = config
        self.field: SymbolicField = self._init_field()
        self.time: float = 0.0
        self.step_count: int = 0

    @abstractmethod
    def step(self) -> None:
        """
        Advance the simulation by one timestep.
        Must be implemented by subclasses.
        """
        ...

    def run(self) -> None:
        print(f"[{self.__class__.__name__}] Starting simulation in mode: {self.config.engine.backend}")
        start = time.perf_counter()

        for _ in range(self.config.defaults.simulation_steps):
            self.step()
            self.step_count += 1

            if self.config.debug.verbose and self.step_count % 100 == 0:
                print(f"[{self.__class__.__name__}] Step {self.step_count}/{self.config.defaults.simulation_steps}")

        end = time.perf_counter()
        export_snapshot(self.field, self.config)
        print(f"[{self.__class__.__name__}] Done. Duration: {end - start:.2f} seconds")

    def _init_field(self) -> SymbolicField:
        from zenoengine.fields.field import SymbolicField
        return SymbolicField(self.config)
