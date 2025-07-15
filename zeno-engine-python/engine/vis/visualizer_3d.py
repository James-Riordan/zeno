import pyvista as pv
import numpy as np

def visualize_3d_field(field: np.ndarray, title: str = "3D Field Visualization") -> None:
    """
    Show a live 3D volume of a scalar field using PyVista.
    """
    grid = pv.UniformGrid()

    # Set grid dimensions
    nx, ny, nz = field.shape
    grid.dimensions = np.array(field.shape) + 1  # +1 for cell-centered to vertex conversion
    grid.spacing = (1, 1, 1)  # Spacing between grid points
    grid.origin = (0, 0, 0)

    # Add field data
    grid.cell_data["ψ"] = field.flatten(order="F")

    # Render
    plotter = pv.Plotter()
    plotter.add_volume(grid, cmap="viridis", opacity="sigmoid", shade=True)
    plotter.add_axes()
    plotter.add_title(title)
    plotter.show()
