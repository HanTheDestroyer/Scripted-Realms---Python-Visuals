
# Chladni Patterns 2D

This project visualizes animated Chladni patterns using GPU-accelerated particles in Python. Each particle moves according to a Chladni pattern equation, creating dynamic and beautiful nodal patterns inspired by vibrating plates.

## Features

- **Real-time animation** of thousands of particles using OpenGL and GPU computation.
- **Chladni pattern transitions**: Patterns change over time with smooth transitions.
- **Highly customizable**: Change the number of particles, pattern parameters, and visual style.

## Requirements

- Python 3.8+
- [moderngl](https://moderngl.readthedocs.io/)
- [moderngl-window](https://github.com/moderngl/moderngl-window)
- [cupy](https://cupy.dev/) (for fast GPU array operations)
- [numpy](https://numpy.org/)

Install dependencies with:

```sh
pip install moderngl moderngl-window cupy numpy
```

## Running

Make sure you change the shader paths to reflect your own documents.

```sh
python animation.py
```

## File Overview

- `animation.py` — Main application and rendering loop.
- `particle.py` — Particle system and Chladni pattern logic.
- `Shaders/particle.vert` — Vertex shader for particle rendering.
- `Shaders/particle.frag` — Fragment shader for particle rendering.

## Customization

- Change the number of particles in `animation.py` (`num_particles`).
- Adjust pattern transition timing and thresholds in `particle.py`.
- Modify shaders in the `Shaders/` folder for different visual effects.

## References

- [Chladni Patterns - Wikipedia](https://en.wikipedia.org/wiki/Chladni_figure)
- [moderngl Documentation](https://moderngl.readthedocs.io/)
- [Patt Vira] (https://www.youtube.com/watch?v=J-siGcsK2k8&)
- [Paul Bourke] (https://paulbourke.net/geometry/chladni/)
---

Enjoy exploring Chladni patterns!
