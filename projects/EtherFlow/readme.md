# EtherFlow

Welcome, Han. This is EtherFlow: a high-performance, GPU-accelerated particle simulation visualized with ModernGL and managed with Python and CuPy. EtherFlow leverages modern OpenGL (via `moderngl`), procedural Perlin noise fields, and one million particles for mesmerizing, real-time fluid-like motion.

> **Note:** This project is optimized for users familiar with Python, ModernGL, and GPU programming concepts.

---

## Features

- **1,000,000 Particles:** Massive, real-time particle simulation.
- **GPU Acceleration:** Uses [CuPy](https://cupy.dev/) for NumPy-compatible GPU arrays.
- **Perlin Noise Fields:** Procedural, smooth vector fields for beautiful fluid motion.
- **ModernGL Rendering:** OpenGL 3.3, programmable shaders (vertex + fragment).
- **Customizable Shaders:** Plug your own GLSL code into the rendering pipeline.
- **Window Management:** Powered by `moderngl_window` for easy display and input handling.

---

## Prerequisites

- Python 3.8+
- A CUDA-capable GPU (for CuPy)
- [ModernGL](https://github.com/moderngl/moderngl)
- [ModernGL-Window](https://github.com/moderngl/moderngl-window)
- [CuPy](https://cupy.dev/)
- [numpy](https://numpy.org/)
- Your own `Particle` and `PerlinNoise2D` classes (see below)

---

## Installation

```sh
pip install moderngl moderngl-window cupy numpy
```

> **Note:** CuPy installation depends on your CUDA version. See [CuPy installation guide](https://docs.cupy.dev/en/stable/install.html).

---

## File Structure

```
etherflow/
├── main.py                # Main simulation code (shown above)
├── particle.py            # Particle system implementation
├── perlin.py              # PerlinNoise2D implementation
└── shaders/
    ├── particle.vert      # Vertex shader (GLSL)
    └── particle.frag      # Fragment shader (GLSL)
```

---

## Usage

```sh
python main.py
```

- The simulation will open a window (1280x1280 by default).
- Watch as particles flow and swirl, driven by dual Perlin noise fields.
- Average field direction is printed to the console every frame.

---

## Configuration

You can tweak parameters in `EtherFlow`:

- `num_particles` (default: 1_000_000)
- `window_size` (default: 1280x1280)
- `max_velocity` (default: 0.0015)
- Perlin noise settings: `seed`, `persistence`, `octaves`, `ranges`

Change shader paths in the `EtherFlow` class to use your own GLSL code.

---

## Dependencies

- [moderngl](https://github.com/moderngl/moderngl)
- [moderngl-window](https://github.com/moderngl/moderngl-window)
- [cupy](https://cupy.dev/)
- [numpy](https://numpy.org/)

---

## Notes

- **You must implement:**  
  - `Particle` class (`particle.py`): Handles particle positions, velocities, buffer updates, shader program, and VAO.
  - `PerlinNoise2D` class (`perlin.py`): Generates 2D Perlin noise arrays compatible with CuPy.
- **Shaders:**  
  - Provide your own `particle.vert` and `particle.frag` GLSL shaders in the `shaders/` directory.  
  - Make sure the paths in the code match your file locations.

---

## Acknowledgements

- This project combines procedural graphics and GPU programming for creative coding explorations.
- Built with tools designed for performance and flexibility in Python.

---
