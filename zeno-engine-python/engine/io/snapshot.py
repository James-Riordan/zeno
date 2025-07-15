import os
import numpy as np

def save_npy(array: np.ndarray, filename: str, output_dir: str = "outputs") -> None:
    """
    Save a NumPy array to a .npy file in the specified directory.
    """
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, filename)
    np.save(path, array)
    print(f"[Snapshot] Saved raw .npy file to {path}")
