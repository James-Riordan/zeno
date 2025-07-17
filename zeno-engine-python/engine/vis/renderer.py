from __future__ import annotations
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from engine.fields.field import SymbolicField
from engine.config.config import PGNSConfig


def render_frame(
    field: SymbolicField,
    config: PGNSConfig,
    step: int,
    avg_fps: float | None = None
) -> np.ndarray:
    """
    Render a grayscale RGB image with step count and FPS overlay.
    Supports 1D, 2D, and 3D (via center slice).
    """
    psi = field.snapshot()
    dim = config.dimension

    # Normalize field values to 0–255
    data = psi.copy()
    if dim == 3:
        mid = data.shape[2] // 2
        data = data[:, :, mid]
    data_norm = (data - data.min()) / (data.max() - data.min() + 1e-8)
    gray = np.uint8(255 * data_norm)

    # Expand grayscale to RGB
    if dim == 1:
        height = 128
        band = np.tile(gray, (height, 1))
        rgb = np.stack([band] * 3, axis=-1)
    else:
        rgb = np.stack([gray] * 3, axis=-1)

    # Create image and draw overlay
    image = Image.fromarray(rgb)
    draw = ImageDraw.Draw(image)
    text = f"Step {step}"
    if avg_fps:
        text += f" | {avg_fps:.2f} FPS"

    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 14)
    except IOError:
        font = ImageFont.load_default()

    draw.text((6, 6), text, fill=(255, 255, 255), font=font)
    return np.array(image)
