from fastapi import FastAPI
from typing import cast
from zenoengine.config.config import PGNSConfig, Dimension, SimMode
from zenoengine.sim.controller import run_simulation
from pathlib import Path
import threading


app = FastAPI(title="Zeno Engine API")

@app.get("/")
def root():
    return {"message": "Zeno Engine is alive!"}

@app.post("/simulate")
def simulate(
    dim: int = 2,
    grid: int = 128,
    steps: int = 500,
    scene: str = "RTI_2D",
    mode: str = "symbolic"
):
    if dim not in (1, 2, 3):
        raise ValueError("dimension must be 1, 2, or 3")
    if mode not in ("symbolic", "classical"):
        raise ValueError("mode must be 'symbolic' or 'classical'")

    config = PGNSConfig(
        dimension=cast(Dimension, dim),
        grid_size=grid,
        total_steps=steps,
        scene=scene,
        mode=cast(SimMode, mode),
        save_video=True,
        save_images=True,
        show_progress=False,
        multithread=True,
    )

    thread = threading.Thread(target=run_simulation, args=(config,))
    thread.start()

    return {
        "status": "started",
        "scene": scene,
        "dim": dim,
        "mode": mode
    }

@app.get("/status")
def status(scene: str = "RTI_2D") -> dict:
    """
    Returns status of a simulation: running, done, or unknown.
    """
    outputs_dir = Path("outputs")
    matching_dirs = list(outputs_dir.glob(f"{scene}_*"))

    if not matching_dirs:
        return {"status": "unknown", "message": "No output found for this scene."}

    latest = max(matching_dirs, key=lambda d: d.stat().st_mtime)
    metrics_file = latest / f"{scene}_metrics.json"

    if metrics_file.exists():
        return {
            "status": "done",
            "path": str(metrics_file),
            "timestamp": latest.name.split("_")[-1],
        }

    return {"status": "running", "output_dir": str(latest)}