import os
import numpy as np
from PIL import Image
from engine.fields.field import SymbolicField
from engine.config.config import PGNSConfig
from engine.io.snapshot import save_npy


def export_snapshot(field: SymbolicField, config: PGNSConfig) -> None:
    """
    Save final field snapshot as both .npy and .png image.
    """
    arr = field.snapshot()
    os.makedirs(config.output_dir, exist_ok=True)

    # Save .npy raw data
    npy_filename = f"{config.scene}_final.npy"
    save_npy(arr, filename=npy_filename, output_dir=config.output_dir)

    # Save image
    norm = (arr - arr.min()) / (arr.max() - arr.min() + 1e-8)
    image_data = np.uint8(norm * 255)

    if config.dimension == 2:
        rgb = np.stack([image_data] * 3, axis=-1)
    elif config.dimension == 1:
        height = 128
        expanded = np.tile(image_data, (height, 1))
        rgb = np.stack([expanded] * 3, axis=-1)
    else:
        print("[Export] Unsupported dimension for image export.")
        return

    img = Image.fromarray(rgb)
    img_path = os.path.join(config.output_dir, f"{config.scene}_final.png")
    img.save(img_path)
    print(f"[Export] Saved image to {img_path}")
