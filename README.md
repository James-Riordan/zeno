# 🧠 Zeno

> A timeless engine for symbolic wave and field simulation — discrete, harmonic, and post-calculus.

Zeno is a dual-stack symbolic physics engine and visualization platform, designed to replace classical PDE solvers with fully symbolic, recursive logic rooted in Partition Geometry, entropy gradients, and wave-based field theory.

It is built for researchers, engineers, and thinkers who seek to simulate energy, heat, curvature, and structure **without calculus**, **without derivatives**, and **without floating-point diffusion** — using symbolic logic alone.

---

## 📐 What Does Zeno Do?

Zeno simulates symbolic field evolution in 1D, 2D, and 3D using equations like:

\[
\frac{∂𝒜}{∂t} = -i \left( ℛ[𝒜] + λ𝒯[𝒜] + κ|𝒜|^2𝒜 + β𝒮^*[𝒜] \right)
\]

Where:
- `𝒜` is the symbolic energy field
- `ℛ[𝒜]` is symbolic curvature via **Partition Geometry**
- `𝒯[𝒜]` is symbolic torsion (antisymmetric twist)
- `|𝒜|²𝒜` is nonlinear self-focusing
- `𝒮*[𝒜]` is symbolic entropy tension

This is known as the **Partition Geometry Navier–Stokes (PGNS)** equation — a discrete symbolic replacement for ∇², ∇·, and ∇× operators in classical PDEs.

---

## 🧰 Monorepo Structure

This repo contains two core projects:

```sh
zeno/
├── zeno-engine-python/ # Symbolic simulation engine (Numba, FastAPI)
├── zeno-viewer/ # UI viewer (SvelteKit, TailwindCSS, Three.js)
├── docker-compose.yml # Full-stack runner (viewer + API)
```

### 🔬 [`zeno-engine-python/`](./zeno-engine-python)

- Runs symbolic simulations (`PGNS`, `REHTE`, etc.)
- Offers both CLI and HTTP API
- Saves `.mp4`, `.gif`, `.npy`, `.csv`, `.json` metrics
- Powered by FastAPI, Numba, and NumPy

### 🌐 [`zeno-viewer/`](./zeno-viewer)

- Web UI for configuring and launching simulations
- Tailwind-powered design, optional Three.js visualizer
- Shows simulation output and status in-browser

---

## 🚀 Quickstart (Dev Mode)

```bash
# Launch both API and Viewer in dev mode
docker-compose -f docker-compose.dev.yml up --build
