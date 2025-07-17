from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, Optional, TYPE_CHECKING

from datetime import datetime
import os


if TYPE_CHECKING:
    from engine.fields.field import SymbolicField

Dimension = Literal[1, 2, 3]
Geometry = Literal["cartesian", "rhombic"]
SceneName = str
SimMode = Literal["symbolic", "classical"]

@dataclass
class PGNSConfig:
    # Core space and simulation
    dimension: Dimension = 2
    grid_size: int = 128
    time_step: float = 0.01
    total_steps: int = 1000
    mode: SimMode = "symbolic"  # symbolic vs classical

    # Geometry and scene
    geometry: Geometry = "cartesian"
    scene: SceneName = "RTI_2D"

    # Output settings
    save_images: bool = True
    save_video: bool = True
    base_output_dir: str = "outputs"
    output_dir: str = field(init=False)

    # Debug / QOL
    show_progress: bool = True
    multithread: bool = True

    # Runtime data (used for rendering overlays)
    field: Optional[SymbolicField] = None

    def __post_init__(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = os.path.join(self.base_output_dir, f"{self.scene}_{timestamp}")
        os.makedirs(self.output_dir, exist_ok=True)
