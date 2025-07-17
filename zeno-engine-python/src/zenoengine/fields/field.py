from __future__ import annotations
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from zenoengine.config.config import PGNSConfig


class SymbolicField:
    def __init__(self, config: PGNSConfig):
        # 👇 Deferred import to avoid circular dependency
        from zenoengine.scenes.scene_registry import SCENES

        self.config = config
        shape = (config.grid_size,) * config.dimension
        self.values: np.ndarray = np.zeros(shape, dtype=np.float64)

        # Use scene-specific initializer
        scene = SCENES.get(config.scene)
        if scene:
            scene.init(self)
        else:
            print(f"[Field] Warning: No initializer found for scene: {config.scene}")

    def apply_delta(self, delta: np.ndarray, dt: float) -> None:
        self.values += delta * dt

    def snapshot(self) -> np.ndarray:
        return self.values.copy()
