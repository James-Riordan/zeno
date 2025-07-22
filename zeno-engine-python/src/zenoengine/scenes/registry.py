from __future__ import annotations
import numpy as np
from typing import Callable
from zenoengine.fields.field import SymbolicField

SceneInitFunc = Callable[[SymbolicField], None]


class SimulationScene:
    def __init__(self, name: str, init: SceneInitFunc):
        self.name = name
        self.init = init


def rti_2d_initializer(field: SymbolicField) -> None:
    arr = field.values
    mid_y = arr.shape[1] // 2
    arr[:, :mid_y] = -1.0
    arr[:, mid_y:] = 1.0
    arr += np.random.normal(scale=0.05, size=arr.shape)


def pulse_1d_initializer(field: SymbolicField) -> None:
    x = np.linspace(-1, 1, field.config.grid_size)
    field.values[:] = np.exp(-100 * x**2)


def checkerboard_2d_initializer(field: SymbolicField) -> None:
    for i in range(field.config.grid_size):
        for j in range(field.config.grid_size):
            field.values[i, j] = (-1) ** (i + j)


def pulse_3d_initializer(field: SymbolicField) -> None:
    size = field.config.grid_size
    x = np.linspace(-1, 1, size)
    y = np.linspace(-1, 1, size)
    z = np.linspace(-1, 1, size)
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    field.values[:] = np.exp(-50 * (X**2 + Y**2 + Z**2))


SCENES: dict[str, SimulationScene] = {
    "RTI_2D": SimulationScene("RTI_2D", rti_2d_initializer),
    "Pulse_1D": SimulationScene("Pulse_1D", pulse_1d_initializer),
    "Checkerboard_2D": SimulationScene("Checkerboard_2D", checkerboard_2d_initializer),
    "Pulse_3D": SimulationScene("Pulse_3D", pulse_3d_initializer),
}
