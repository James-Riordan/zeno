from __future__ import annotations
import os
import json
import csv
from engine.config.config import PGNSConfig


def export_benchmark_metrics(
    config: PGNSConfig,
    total_steps: int,
    total_time: float
) -> None:
    """
    Export benchmark performance metrics (steps, total time, FPS) as JSON and CSV.
    Compatible with plotting tools and reproducibility audits.
    """
    os.makedirs(config.output_dir, exist_ok=True)

    avg_fps = total_steps / total_time if total_time > 0 else 0.0

    metrics = {
        "scene": config.scene,
        "mode": config.mode,
        "dimension": config.dimension,
        "grid_size": config.grid_size,
        "steps": total_steps,
        "time_seconds": round(total_time, 4),
        "avg_fps": round(avg_fps, 4),
        "multithread": config.multithread,
    }

    json_path = os.path.join(config.output_dir, f"{config.scene}_{config.mode}_metrics.json")
    with open(json_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"[Benchmark] Exported JSON metrics to {json_path}")

    csv_path = os.path.join(config.output_dir, f"{config.scene}_{config.mode}_metrics.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=metrics.keys())
        writer.writeheader()
        writer.writerow(metrics)
    print(f"[Benchmark] Exported CSV metrics to {csv_path}")
