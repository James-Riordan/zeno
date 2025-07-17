from __future__ import annotations

import argparse
from engine.config.config import PGNSConfig
from engine.sim.controller import run_simulation


def parse_args() -> PGNSConfig:
    parser = argparse.ArgumentParser(description="Zeno Engine Simulation Runner")

    parser.add_argument(
        "--mode", type=str, default="symbolic", choices=["symbolic", "classical"],
        help="Simulation mode to run"
    )
    parser.add_argument(
        "--scene", type=str, default="RTI_2D",
        help="Simulation scene to initialize"
    )
    parser.add_argument(
        "--steps", type=int, default=500,
        help="Total simulation steps"
    )
    parser.add_argument(
        "--grid", type=int, default=128,
        help="Grid size (N x N or N x N x N)"
    )
    parser.add_argument(
        "--dim", type=int, default=2, choices=[1, 2, 3],
        help="Number of spatial dimensions"
    )
    parser.add_argument(
        "--output", type=str, default="outputs",
        help="Directory to save outputs"
    )
    parser.add_argument(
        "--no-video", action="store_true",
        help="Disable MP4 export"
    )
    parser.add_argument(
        "--no-image", action="store_true",
        help="Disable PNG export"
    )
    parser.add_argument(
        "--no-thread", action="store_true",
        help="Disable multithreading"
    )
    parser.add_argument(
        "--silent", action="store_true",
        help="Suppress per-step logging"
    )

    args = parser.parse_args()

    return PGNSConfig(
        dimension=args.dim,
        grid_size=args.grid,
        total_steps=args.steps,
        scene=args.scene,
        mode=args.mode,
        base_output_dir=args.output,
        save_video=not args.no_video,
        save_images=not args.no_image,
        multithread=not args.no_thread,
        show_progress=not args.silent,
    )


def main() -> None:
    config = parse_args()
    print(f"🧠 Zeno Engine: Running {config.mode} simulation on scene '{config.scene}' "
          f"({config.dimension}D, {config.grid_size}x grid, {config.total_steps} steps)")
    run_simulation(config)


if __name__ == "__main__":
    main()
