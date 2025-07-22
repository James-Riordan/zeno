from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal, Tuple, Any

# -----------------------------
# 🔢 Enum-like type literals
# -----------------------------
BaseSystem = Literal["base10", "base12"]
Dimension = Literal[1, 2, 3]
SimMode = Literal["symbolic", "classical"]
LatticeType = Literal["grid", "hex", "rhombic_dodecahedron", "torus", "partition"]
Geometry = Literal["cartesian", "rhombic"]

# -----------------------------
# ⚙️ Sub-config components
# -----------------------------

class MathConfig(BaseModel):
    number_base: int = Field(default=10, description="Numerical base for all math operations (10 or 12)")

class DefaultsConfig(BaseModel):
    lattice_type: LatticeType = Field(default="grid")
    dimensions: Dimension = Field(default=2)
    grid_size: Tuple[int, int] = Field(default=(64, 64))
    field: str = Field(default="rti")
    operator: str = Field(default="pgns")
    simulation_steps: int = Field(default=1000)
    output_format: str = Field(default="npy")
    mode: SimMode = Field(default="symbolic")
    time_step: float = Field(default=1.0)
    scene: str = Field(default="default")

class GUIConfig(BaseModel):
    auto_launch: bool = Field(default=True)
    theme: str = Field(default="dark")
    default_zoom: float = Field(default=1.0)

class EngineConfig(BaseModel):
    num_threads: Any = Field(default="auto")  # Can be int or "auto"
    use_numba: bool = Field(default=True)
    backend: SimMode = Field(default="symbolic")

class OutputConfig(BaseModel):
    save_dir: str = Field(default="./output")
    formats: list[str] = Field(default_factory=lambda: ["png", "mp4", "json"])
    enable_metrics: bool = Field(default=True)

class DebugConfig(BaseModel):
    verbose: bool = Field(default=False)
    log_level: str = Field(default="info")
    profile: bool = Field(default=False)

# -----------------------------
# 🧠 Top-level config wrapper
# -----------------------------

class ZenoConfig(BaseModel):
    math: MathConfig
    defaults: DefaultsConfig
    gui: GUIConfig
    engine: EngineConfig
    output: OutputConfig
    debug: DebugConfig
