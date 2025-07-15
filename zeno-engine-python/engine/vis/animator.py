from __future__ import annotations
import os
import time
import numpy as np
import imageio.v3 as iio
from typing import List, Optional, TYPE_CHECKING

from zeno.config.config import PGNSConfig

if TYPE_CHECKING:
    from zeno.fields.field import SymbolicField


class FrameCollector:
    def __init__(self, config: PGNSConfig):
        self.frames: List[np.ndarray] = []
        self.config = config
        self.start_time = time.perf_counter()
        self.last_frame_time = self.start_time
        self.fps_log: List[float] = []

    def add(self, frame: np.ndarray, step: int) -> None:
        now = time.perf_counter()
        delta = now - self.last_frame_time
        self.last_frame_time = now

        if delta > 0:
            self.fps_log.append(1.0 / delta)

        avg_fps = sum(self.fps_log) / len(self.fps_log) if self.fps_log else None

        # ⛑️ Runtime check for safety
        if self.config.field is None:
            raise ValueError("[FrameCollector] config.field is None — field must be assigned before rendering.")

        from zeno.vis.renderer import render_frame  # Local to avoid cycles
        frame_with_overlay = render_frame(
            field=self.config.field,
            config=self.config,
            step=step,
            avg_fps=avg_fps,
        )
        self.frames.append(frame_with_overlay)

    def save_gif(self) -> None:
        if not self.frames or not self.config.save_images:
            return

        os.makedirs(self.config.output_dir, exist_ok=True)
        path = os.path.join(self.config.output_dir, f"{self.config.scene}_evolution.gif")
        iio.imwrite(path, self.frames, duration=1 / 10, loop=0)
        print(f"[Animator] Saved GIF: {path}")

    def save_mp4(self) -> None:
        if not self.frames or not self.config.save_video:
            return

        os.makedirs(self.config.output_dir, exist_ok=True)
        path = os.path.join(self.config.output_dir, f"{self.config.scene}_evolution.mp4")
        iio.imwrite(path, self.frames, fps=30)
        print(f"[Animator] Saved MP4: {path}")
