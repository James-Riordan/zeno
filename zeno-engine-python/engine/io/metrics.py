import os
import json
import csv
import numpy as np

class MetricTracker:
    def __init__(self, scene: str, output_dir: str = "outputs"):
        self.scene = scene
        self.output_dir = output_dir
        self.data = []

    def record(self, step: int, time: float, psi: np.ndarray, R: np.ndarray, T: np.ndarray) -> None:
        metrics = {
            "step": step,
            "time": round(time, 6),
            "field_energy": float(np.sum(np.abs(psi))),
            "curvature_energy": float(np.sum(np.abs(R))),
            "torsion_energy": float(np.sum(np.abs(T)))
        }
        self.data.append(metrics)

    def export_json(self) -> None:
        path = os.path.join(self.output_dir, f"{self.scene}_metrics.json")
        os.makedirs(self.output_dir, exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.data, f, indent=2)
        print(f"[Metrics] Exported JSON: {path}")

    def export_csv(self) -> None:
        if not self.data:
            return
        path = os.path.join(self.output_dir, f"{self.scene}_metrics.csv")
        os.makedirs(self.output_dir, exist_ok=True)
        with open(path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.data[0].keys())
            writer.writeheader()
            writer.writerows(self.data)
        print(f"[Metrics] Exported CSV: {path}")

    def summarize(self) -> None:
        if not self.data:
            return
        last = self.data[-1]
        print(
            f"[Metrics] Final step: {last['step']}, "
            f"psi={last['field_energy']:.2f}, "
            f"R={last['curvature_energy']:.2f}, "
            f"T={last['torsion_energy']:.2f}"
        )
