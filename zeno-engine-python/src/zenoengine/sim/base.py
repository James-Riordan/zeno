from __future__ import annotations
import time
from abc import ABC, abstractmethod
from zenoengine.config.config import PGNSConfig
from zenoengine.fields.field import SymbolicField
from zenoengine.io.export import export_snapshot


class BaseSimulation(ABC):
    def __init__(self, config: PGNSConfig):
        self.config = config
        self.field = SymbolicField(config)
        self.time: float = 0.0
        self.step_count: int = 0

    @abstractmethod
    def step(self) -> None:
        """
        Advance the simulation by one step.
        Must be implemented by subclasses.
        """
        ...

    def run(self) -> None:
        print(f"[{self.__class__.__name__}] Starting simulation in mode: {self.config.mode}")
        start = time.perf_counter()

        for _ in range(self.config.total_steps):
            self.step()
            if self.config.show_progress and self.step_count % 100 == 0:
                print(f"[{self.__class__.__name__}] Step {self.step_count}/{self.config.total_steps}")

        end = time.perf_counter()
        export_snapshot(self.field, self.config)
        print(f"[{self.__class__.__name__}] Done. Duration: {end - start:.2f} seconds")
