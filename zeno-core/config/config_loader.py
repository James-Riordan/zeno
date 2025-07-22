from __future__ import annotations
from typing import Any, Dict, Optional

from config.types import ZenoConfig


def load_config_with_overrides(
    toml_path: Optional[str] = None,
    cli_overrides: Optional[Dict[str, Any]] = None
) -> ZenoConfig:
    """
    Load the full ZenoConfig by:
    1. Parsing the TOML config file (default: config.toml or $ZENO_CONFIG_PATH)
    2. Applying any CLI overrides as final values

    Args:
        toml_path: Optional path to a config TOML file (overrides env default)
        cli_overrides: A flat dictionary with override values like
            {
                "defaults.lattice_type": "hex",
                "engine.num_threads": 4
            }

    Returns:
        A complete ZenoConfig instance
    """
    # 1. Load from TOML file
    config = ZenoConfig.load(path=toml_path) if toml_path else ZenoConfig.load()

    # 2. Apply CLI overrides (dot-paths)
    if cli_overrides:
        for dotted_path, value in cli_overrides.items():
            apply_override(config, dotted_path, value)

    return config


def apply_override(config: ZenoConfig, dotted_path: str, value: Any) -> None:
    """
    Apply a value override to a config object via dot-path syntax.

    Example:
        dotted_path: "engine.num_threads"
        value: 8
    """
    parts = dotted_path.split(".")
    target = config

    for attr in parts[:-1]:
        if not hasattr(target, attr):
            raise AttributeError(f"[Config] No such section: '{attr}' in path '{dotted_path}'")
        target = getattr(target, attr)

    final_attr = parts[-1]
    if not hasattr(target, final_attr):
        raise AttributeError(f"[Config] No such field: '{final_attr}' in path '{dotted_path}'")

    setattr(target, final_attr, value)
