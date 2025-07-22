from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal, Optional, Tuple, Any
import os
import toml

# === Type Aliases ===
BaseSystem = Literal["base10", "base12"]
SimMode = Literal["symbolic", "classical"]
Dimension = Literal[1, 2, 3]
LatticeType = Literal["grid", "hex", "rhombic_dodecahedron", "torus", "partition"]
Geometry = Literal["cartesian", "rhombic"]

CONFIG_PATH = os.getenv("ZENO_CONFIG_PATH", "config.toml")

# === Config Sections ===

@dataclass
class MathConfig:
    number_base: int = 10  # 10 or 12 for base-10/base-12 logic

@dataclass
class DefaultsConfig:
    lattice_type: LatticeType = "grid"
    dimensions: Dimension = 2
    grid_size: Tuple[int, int] = (64, 64)
    field: str = "rti"
    operator: str = "pgns"
    simulation_steps: int = 1000
    output_format: str = "npy"

@dataclass
class GUIConfig:
    auto_launch: bool = True
    theme: str = "dark"
    default_zoom: float = 1.0

@dataclass
class EngineConfig:
    num_threads: Any = "auto"  # int or "auto"
    use_numba: bool = True
    backend: SimMode = "symbolic"

@dataclass
class OutputConfig:
    save_dir: str = "./output"
    formats: list[str] = field(default_factory=lambda: ["png", "mp4", "json"])
    enable_metrics: bool = True

@dataclass
class DebugConfig:
    verbose: bool = False
    log_level: str = "info"
    profile: bool = False

# === Unified Top-Level Config ===

@dataclass
class ZenoConfig:
    math: MathConfig
    defaults: DefaultsConfig
    gui: GUIConfig
    engine: EngineConfig
    output: OutputConfig
    debug: DebugConfig

    @classmethod
    def load(cls, path: str = CONFIG_PATH) -> ZenoConfig:
        raw = toml.load(path)
        return cls(
            math=MathConfig(**raw.get("math", {})),
            defaults=DefaultsConfig(**raw.get("defaults", {})),
            gui=GUIConfig(**raw.get("gui", {})),
            engine=EngineConfig(**raw.get("engine", {})),
            output=OutputConfig(**raw.get("output", {})),
            debug=DebugConfig(**raw.get("debug", {})),
        )
