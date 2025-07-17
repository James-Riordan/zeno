from __future__ import annotations
import numpy as np
from typing import Callable, TYPE_CHECKING

from zenoengine.config.config import PGNSConfig

# `if TYPE_CHECKING: ...` resolves circular import because
# `SymbolicField` is no longer accessed at runtime
# and instead is just hinted at for static type checking
if TYPE_CHECKING:
    from zenoengine.fields.field import SymbolicField  # only used for type hints

SceneInitFunc = Callable[[ 'SymbolicField' ], None]  # string-based forward reference

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

SCENES: dict[str, SimulationScene] = {
    "RTI_2D": SimulationScene("RTI_2D", rti_2d_initializer),
}
