
# Night Sky Animation

This project creates a real-time animated night sky using GPU-accelerated Perlin noise clouds and glowing particles (e.g., stars) with Python, ModernGL, and CuPy. The animation combines procedural cloud textures and dynamic particles for a visually rich generative scene.

## Features

- **Procedural Clouds:** Animated using 3D Perlin noise, rendered as textures.
- **Particles:** Customizable glowing points (stars, etc.) rendered with shaders.
- **GPU Acceleration:** Uses ModernGL for fast rendering and CuPy for efficient array operations.

## Requirements

- Python 3.8+
- [moderngl](https://moderngl.readthedocs.io/)
- [moderngl-window](https://github.com/moderngl/moderngl-window)
- [cupy](https://cupy.dev/)
- [numpy](https://numpy.org/)

Install dependencies with:
```sh
pip install moderngl moderngl-window cupy numpy
```

## Usage

1. **Clone or download this repository.**
2. **Update shader file paths:**  
   In `night_sky.py`, make sure the `vertex_shader` and `fragment_shader` paths for both clouds and particles point to the correct locations on your system.  
   Example:
   ```python
   vertex_shader=r'path/to/your/shaders/particle.vert',
   fragment_shader=r'path/to/your/shaders/particle.frag'
   ```
3. **Run the animation:**
   ```sh
   python night_sky.py
   ```

## File Overview

- `night_sky.py` — Main application and rendering loop.
- `clouds.py` — Cloud generation and rendering logic using Perlin noise.
- `particle.py` — Particle system for rendering stars or other glowing points.
- `shaders/` — Vertex and fragment shaders for clouds and particles.

## Customization

- **Number of particles:** Change `num_particles` in `night_sky.py`.
- **Cloud appearance:** Adjust `octaves`, `persistence`, and `seed` in the `Clouds` object.
- **Particle appearance:** Modify the particle shaders or parameters.
- **Shader locations:**  
  Update the `vertex_shader` and `fragment_shader` arguments to match your file system.

## Example Shader Path Change

```python
vertex_shader=r'C:/Users/yourname/Documents/Creative Coding/P06 - Night Sky/shaders/particle.vert',
fragment_shader=r'C:/Users/yourname/Documents/Creative Coding/P06 - Night Sky/shaders/particle.frag'
```

## License

This project is for educational and creative coding purposes.

---

Enjoy your generative night sky!
