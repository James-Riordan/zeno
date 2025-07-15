from __future__ import annotations
import argparse
import os
import subprocess
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw


def run_sim(mode: str, scene: str, steps: int, grid: int, silent: bool = False) -> str:
    tag = f"{scene}_{mode}"
    output_dir = "outputs"
    csv_path = os.path.join(output_dir, f"{tag}_metrics.csv")

    cmd = [
        "python", "entry.py",
        "--mode", mode,
        "--scene", scene,
        "--steps", str(steps),
        "--grid", str(grid),
    ]
    if silent:
        cmd.append("--silent")

    print(f"[Compare] Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"[ERROR] Expected CSV not found: {csv_path}")
    return csv_path


def plot_metrics_comparison(path1: str, path2: str, tag1: str, tag2: str, out_path: str) -> None:
    df1 = pd.read_csv(path1)
    df2 = pd.read_csv(path2)

    canvas = np.ones((512, 1024, 3), dtype=np.uint8) * 255

    def plot_line(canvas: np.ndarray, values: np.ndarray, color: tuple[int, int, int], offset_y: int):
        if len(values) == 0:
            return
        h, w = canvas.shape[:2]
        norm = (values - np.min(values)) / (np.max(values) - np.min(values) + 1e-8)
        for i in range(1, len(values)):
            x1 = int((i - 1) / len(values) * w)
            x2 = int(i / len(values) * w)
            y1 = h - int(norm[i - 1] * 200) - offset_y
            y2 = h - int(norm[i] * 200) - offset_y
            if 0 <= x1 < w and 0 <= x2 < w and 0 <= y1 < h and 0 <= y2 < h:
                canvas = draw_line(canvas, x1, y1, x2, y2, color)

    def draw_line(img: np.ndarray, x0: int, y0: int, x1: int, y1: int, color: tuple[int, int, int]):
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            if 0 <= x0 < img.shape[1] and 0 <= y0 < img.shape[0]:
                img[y0, x0] = color
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy
        return img

    # Plot psi, R, T for both
    plot_line(canvas, df1["psi"].to_numpy(), color=(0, 0, 255), offset_y=100)
    plot_line(canvas, df1["R"].to_numpy(),   color=(255, 0, 0), offset_y=200)
    plot_line(canvas, df1["T"].to_numpy(),   color=(0, 200, 0), offset_y=300)

    plot_line(canvas, df2["psi"].to_numpy(), color=(0, 0, 100), offset_y=100)
    plot_line(canvas, df2["R"].to_numpy(),   color=(100, 0, 0), offset_y=200)
    plot_line(canvas, df2["T"].to_numpy(),   color=(0, 100, 0), offset_y=300)

    image = Image.fromarray(canvas)
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), f"{tag1} vs {tag2}", fill=(0, 0, 0))
    image.save(out_path)
    print(f"[Compare] Plot saved: {out_path}")


def compare_modes_and_scenes(
    scene1: str,
    mode1: str,
    scene2: str,
    mode2: str,
    steps: int,
    grid: int,
    silent: bool = False
):
    tag1 = f"{scene1}_{mode1}"
    tag2 = f"{scene2}_{mode2}"
    print(f"🧪 Comparing: {tag1} vs {tag2}")

    path1 = run_sim(mode1, scene1, steps, grid, silent)
    path2 = run_sim(mode2, scene2, steps, grid, silent)

    out_path = f"outputs/{tag1}_vs_{tag2}_comparison.png"
    plot_metrics_comparison(path1, path2, tag1, tag2, out_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare two Zeno Engine simulation outputs")
    parser.add_argument("--scene1", type=str, required=True, help="Scene name for first simulation")
    parser.add_argument("--mode1", type=str, required=True, help="Mode for first simulation (symbolic/classical)")
    parser.add_argument("--scene2", type=str, required=True, help="Scene name for second simulation")
    parser.add_argument("--mode2", type=str, required=True, help="Mode for second simulation (symbolic/classical)")
    parser.add_argument("--steps", type=int, default=500, help="Total steps")
    parser.add_argument("--grid", type=int, default=128, help="Grid size")
    parser.add_argument("--silent", action="store_true", help="Suppress verbose logs")
    args = parser.parse_args()

    compare_modes_and_scenes(
        scene1=args.scene1,
        mode1=args.mode1,
        scene2=args.scene2,
        mode2=args.mode2,
        steps=args.steps,
        grid=args.grid,
        silent=args.silent
    )
