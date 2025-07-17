# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

# from zenoengine.fields.field import SymbolicField
# from zenoengine.config.config import PGNSConfig

# def render_frame(field: SymbolicField, config: PGNSConfig, step_count: int) -> np.ndarray:
#     data = field.snapshot()
#     fig, ax = plt.subplots(figsize=(6, 6))
#     canvas = FigureCanvas(fig)

#     if config.dimension == 2:
#         im = ax.imshow(data.T, origin="lower", cmap="plasma")
#         ax.set_title(f"{config.scene} | Step {step_count}")
#         fig.colorbar(im, ax=ax)
#     elif config.dimension == 1:
#         ax.plot(data)
#         ax.set_ylim(-1.5, 1.5)
#         ax.set_title(f"{config.scene} | Step {step_count}")
#     else:
#         raise NotImplementedError("Only 1D and 2D rendering supported for now.")

#     canvas.draw()
#     width, height = canvas.get_width_height()
#     img = np.frombuffer(canvas.buffer_rgba(), dtype=np.uint8).reshape((height, width, 4))
#     img = img[:, :, :3]  # remove alpha
#     plt.close(fig)
#     return img
