from __future__ import annotations
import numpy as np

from zenoengine.engine.base import BaseSimulation
from from zenocore.config.types import ZenoConfig
from zenoengine.core.operators.main import symbolic_pgns_operator
from zenoengine.core.operators.curvature import curvature_operator
from zenoengine.core.operators.torsion import torsion_operator
from zenoengine.vis.renderer import render_frame
from zenoengine.vis.animator import FrameCollector
from zenoengine.io.metrics import MetricTracker


class PGNSSimulation(BaseSimulation):
    """
    Partition Geometry Navier–Stokes Simulation:
    ∂𝒜/∂t = -i (ℛ[𝒜] + λ·𝒯[𝒜] + κ·|𝒜|²·𝒜 + β·𝒮*[𝒜])
    """

    def __init__(self, config: ZenoConfig):
        super().__init__(config)

        self.animator = FrameCollector(config)
        self.metrics = MetricTracker(
            scene=config.defaults.field,
            output_dir=config.output.save_dir
        )

        # Symbolic coefficients — these can later be passed via config.toml
        self.lambda_ = 0.4
        self.kappa = 0.9
        self.beta = 0.3

    def step(self) -> None:
        psi = self.field.values
        dim = self.config.defaults.dimensions

        # Composite symbolic PGNS operator
        delta = symbolic_pgns_operator(
            psi=psi,
            dim=dim,
            lambda_=self.lambda_,
            kappa=self.kappa,
            beta=self.beta
        )

        # Apply update
        self.field.apply_delta(delta, self.config.defaults.simulation_steps)
        self.time += self.config.defaults.simulation_steps
        self.step_count += 1

        # Live render (1D and 2D only for now)
        if dim in (1, 2):
            frame = render_frame(self.field, self.config, step=self.step_count)
            self.animator.add(frame, step=self.step_count)

        # Track symbolic operators for metrics
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
