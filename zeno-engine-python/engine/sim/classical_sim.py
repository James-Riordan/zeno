from __future__ import annotations
import numpy as np

from engine.sim.base import BaseSimulation
from engine.config.config import PGNSConfig
from engine.utils.diff_ops import compute_laplacian_nd
from engine.vis.renderer import render_frame
from engine.vis.animator import FrameCollector
from engine.io.metrics import MetricTracker


class ClassicalSimulation(BaseSimulation):
    def __init__(self, config: PGNSConfig):
        super().__init__(config)
        self.animator = FrameCollector(config)
        self.metrics = MetricTracker(scene=config.scene, output_dir=config.output_dir)

    def step(self) -> None:
        delta = compute_laplacian_nd(self.field.values, self.config.dimension)
        self.field.apply_delta(delta, self.config.time_step)
        self.time += self.config.time_step
        self.step_count += 1

        # Set runtime field reference for overlay rendering
        self.config.field = self.field

        if self.config.dimension in (1, 2):
            frame = render_frame(self.field, self.config, step=self.step_count)
            self.animator.add(frame, step=self.step_count)

        self.metrics.record(
            self.step_count,
            self.time,
            psi=self.field.values.copy(),
            R=np.zeros_like(self.field.values),
            T=np.zeros_like(self.field.values)
        )

    def run(self) -> None:
        super().run()
        self.animator.save_gif()
        self.animator.save_mp4()
        self.metrics.export_json()
        self.metrics.export_csv()
        self.metrics.summarize()
