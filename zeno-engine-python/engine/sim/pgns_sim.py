from __future__ import annotations
import numpy as np

from engine.sim.base import BaseSimulation
from engine.config.config import PGNSConfig
from engine.core.operators.main import symbolic_pgns_operator
from engine.core.operators.curvature import curvature_operator
from engine.core.operators.torsion import torsion_operator
from engine.vis.renderer import render_frame
from engine.vis.animator import FrameCollector
from engine.io.metrics import MetricTracker


class PGNSimulation(BaseSimulation):
    """
    Partition Geometry Navier–Stokes (PGNS) Simulation:
    ∂𝒜/∂t = -i (ℛ[𝒜] + λ·𝒯[𝒜] + κ·|𝒜|²·𝒜 + β·𝒮*[𝒜])
    """

    def __init__(self, config: PGNSConfig):
        super().__init__(config)

        self.animator = FrameCollector(config)
        self.metrics = MetricTracker(
            scene=config.scene,
            output_dir=config.output_dir
        )

        # Symbolic coefficients
        self.lambda_ = 0.4
        self.kappa = 0.9
        self.beta = 0.3

    def step(self) -> None:
        psi = self.field.values
        dim = self.config.dimension

        # Composite symbolic operator
        delta = symbolic_pgns_operator(
            psi=psi,
            dim=dim,
            lambda_=self.lambda_,
            kappa=self.kappa,
            beta=self.beta
        )

        # Apply field update
        self.field.apply_delta(delta, self.config.time_step)
        self.time += self.config.time_step
        self.step_count += 1
        self.config.field = self.field

        # Optional live render
        if dim in (1, 2):
            frame = render_frame(self.field, self.config, step=self.step_count)
            self.animator.add(frame, step=self.step_count)

        # Metrics: selectively recompute R and T for export
        R = curvature_operator(psi, dim)
        T = torsion_operator(psi, dim)

        self.metrics.record(
            step=self.step_count,
            time=self.time,
            psi=psi.copy(),
            R=R.copy(),
            T=T.copy()
        )

    def run(self) -> None:
        super().run()
        self.animator.save_gif()
        self.animator.save_mp4()
        self.metrics.export_json()
        self.metrics.export_csv()
        self.metrics.summarize()
