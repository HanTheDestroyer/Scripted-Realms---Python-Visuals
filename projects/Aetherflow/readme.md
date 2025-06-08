# Aetherflow

Aetherflow is a real-time GPU-accelerated particle flow visualizer using Perlin noise and curl fields, built with Python, ModernGL, and CuPy. Each particle's color and motion are determined by the local curl of a Perlin noise field, creating mesmerizing, fluid-like patterns.

---

## Features

- 100,000+ particles animated in real time
- GPU-based computation and rendering (ModernGL + CuPy)
- Perlin noise-driven curl field for natural motion
- Color mapped to particle velocity
- Highly customizable and efficient

---

## Setup

1. **Install dependencies:**
   - Python 3.8+
   - [moderngl](https://moderngl.readthedocs.io/)
   - [moderngl-window](https://github.com/moderngl/moderngl-window)
   - [cupy](https://cupy.dev/)
   - numpy

2. **Set shader paths:**
   - In `aetherflow.py`, ensure the `vertex_shader` and `fragment_shader` paths point to your local shader files:
     ```
     vertex_shader='path/to/particle.vert',
     fragment_shader='path/to/particle.frag'
     ```

3. **Run the project:**
   ```bash
   python aetherflow.py
   ```

---

## Example Output

![Aetherflow Example](path/to/example_image.png)
*Replace with your own screenshot.*

---

## Notes

- Make sure your GPU supports OpenGL 3.3 or higher.
- The default window size is 1280x1280 (square).
- Particle and field parameters can be tuned in `aetherflow.py`.
- If you see a blank window, check your shader paths and ensure all dependencies are installed.

---

Enjoy exploring the flow!
