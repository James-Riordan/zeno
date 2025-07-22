from __future__ import annotations

import numpy as np
from zenoengine.engine.base import BaseSimulation
from from zenocore.config.types import ZenoConfig
from zenoengine.core.operators.curvature import curvature_operator
from zenoengine.core.operators.topology import topology_operator
from zenoengine.core.operators.entropy import entropy_operator
from zenoengine.vis.renderer import render_frame
from zenoengine.vis.animator import FrameCollector
from zenoengine.io.metrics import MetricTracker


class REHTESimulation(BaseSimulation):
    """
    Ramanujan Energy Heat Transfer Equation (REHTE):
    ∂𝒜/∂t = -i (ℛ[𝒜] + β·𝒮*[𝒜] + λ·𝒯[𝒜])

    ℛ = symbolic curvature (diffusion)
    𝒮* = symbolic entropy gradient
    𝒯 = symbolic topological memory
    """

    def __init__(self, config: ZenoConfig):
        super().__init__(config)

        self.animator = FrameCollector(config)
        self.metrics = MetricTracker(
            scene=config.defaults.scene,
            output_dir=config.output.save_dir
        )

        # Symbolic constants
        self.lambda_ = 0.4
        self.beta = 0.3

    def step(self) -> None:
        psi = self.field.values
        dim = self.config.defaults.dimensions

        # Symbolic composite operator
        R = curvature_operator(psi, dim)
        S = entropy_operator(psi, dim)
        T = topology_operator(psi, dim)

        delta = -1j * (R + self.beta * S + self.lambda_ * T)

        # Apply symbolic update
        self.field.apply_delta(delta, self.config.defaults.time_step)
        self.time += self.config.defaults.time_step
        self.step_count += 1

        # Optional frame rendering
        if dim in (1, 2):
            frame = render_frame(self.field, self.config, step=self.step_count)
            self.animator.add(frame, step=self.step_count)

        # Save metrics
        self.metrics.record(
            step=self.step_count,
            time=self.time,
            psi=psi.copy(),
            R=R.copy(),
            S=S.copy(),
            T=T.copy()
        )

    def run(self) -> None:
        super().run()
        self.animator.save_gif()
        self.animator.save_mp4()
        self.metrics.export_json()
        self.metrics.export_csv()
        self.metrics.summarize()
