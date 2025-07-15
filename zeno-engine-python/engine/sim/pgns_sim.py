from __future__ import annotations
from zeno.sim.base import BaseSimulation
from zeno.core.operators import symbolic_pgns_operator
from zeno.io.metrics import MetricTracker
from zeno.vis.animator import FrameCollector
from zeno.vis.renderer import render_frame

class PGNSSimulation(BaseSimulation):
    def __init__(self, config):
        super().__init__(config)
        self.metrics = MetricTracker(config.scene, config.output_dir)
        self.animator = FrameCollector(config)
        self.config.field = self.field  # 👈 Enables overlay support in render_frame

    def step(self) -> None:
        delta = symbolic_pgns_operator(self.field)
        self.field.apply_delta(delta, self.config.time_step)
        self.time += self.config.time_step
        self.step_count += 1

        if self.config.dimension in (1, 2):
            frame = render_frame(self.field, self.config, self.step_count)
            self.animator.add(frame, step=self.step_count)

        self.metrics.record(
            step=self.step_count,
            time=self.time,
            psi=self.field.values.copy(),
            R=self.cached_curvature,
            T=self.cached_torsion,
        )

    def run(self) -> None:
        super().run()
        self.animator.save_gif()
        self.animator.save_mp4()
        self.metrics.export_json()
        self.metrics.export_csv()
        self.metrics.summarize()

    @property
    def cached_curvature(self):
        from zeno.core.operators import cached_last_curvature
        return cached_last_curvature

    @property
    def cached_torsion(self):
        from zeno.core.operators import cached_last_torsion
        return cached_last_torsion
