from __future__ import annotations

import argparse
from typing import Dict, Any

from zenoengine.config.config_loader import load_config_with_overrides
from zenoengine.sim.controller import run_simulation


def parse_cli_args() -> tuple[dict[str, Any], str | None]:
    """
    Parse CLI arguments and return overrides as a flat dictionary with dot-paths.
    """
    parser = argparse.ArgumentParser(description="Zeno Engine Simulation CLI")

    parser.add_argument("--scene", type=str, help="Simulation scene name")
    parser.add_argument("--dim", type=int, choices=[1, 2, 3], help="Number of dimensions")
    parser.add_argument("--grid", type=int, help="Grid size (assumes NxN or NxNxN)")
    parser.add_argument("--steps", type=int, help="Total simulation steps")
    parser.add_argument("--lattice", type=str, help="Lattice type (grid, hex, etc.)")
    parser.add_argument("--mode", type=str, choices=["symbolic", "classical"], help="Simulation mode")
    parser.add_argument("--threads", type=int, help="Thread count (or 0 to disable multithreading)")
    parser.add_argument("--base", type=str, choices=["base10", "base12"], help="Numerical base system")
    parser.add_argument("--no-video", action="store_true", help="Disable MP4 export")
    parser.add_argument("--no-image", action="store_true", help="Disable PNG export")
    parser.add_argument("--silent", action="store_true", help="Suppress per-step logging")
    parser.add_argument("--config", type=str, help="Optional TOML config path")

    args = parser.parse_args()

    overrides = {}

    # Map CLI to dot-path overrides
    if args.scene:
        overrides["defaults.field"] = args.scene
        overrides["defaults.operator"] = "pgns"  # just a default assumption for now
    if args.dim:
        overrides["defaults.dimensions"] = args.dim
    if args.grid:
        overrides["defaults.grid_size"] = (args.grid,) * args.dim if args.dim else (args.grid, args.grid)
    if args.steps:
        overrides["defaults.simulation_steps"] = args.steps
    if args.lattice:
        overrides["defaults.lattice_type"] = args.lattice
    if args.mode:
        overrides["engine.backend"] = args.mode
    if args.threads is not None:
        overrides["engine.num_threads"] = args.threads if args.threads > 0 else "none"
    if args.base:
        overrides["math.number_base"] = 10 if args.base == "base10" else 12
    if args.no_video:
        overrides["output.formats"] = ["png", "json"]
    if args.no_image:
        formats = overrides.get("output.formats", ["png", "mp4", "json"])
        overrides["output.formats"] = [f for f in formats if f != "png"]
    if args.silent:
        overrides["debug.verbose"] = False
        overrides["debug.log_level"] = "warn"

    return overrides, args.config


def main() -> None:
    overrides, config_path = parse_cli_args()

    config = load_config_with_overrides(
        toml_path=config_path,
        cli_overrides=overrides
    )


    print(f"🧠 Zeno Engine — Launching simulation: {config.defaults.field} "
          f"({config.defaults.dimensions}D, lattice={config.defaults.lattice_type})")

    run_simulation(config)


if __name__ == "__main__":
    main()
