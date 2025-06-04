
# Perlin Noise Algorithms in Python

This project provides 1D, 2D, and 3D Perlin noise implementations in pure Python using NumPy. It includes visualization utilities for each dimension and is suitable for generative art, procedural textures, and simulations.

## Features

- **1D Perlin Noise:** Generate smooth random sequences.
- **2D Perlin Noise:** Create textures and heightmaps.
- **3D Perlin Noise:** Useful for volumetric data and animations.
- **Customizable:** Control octaves, persistence, frequency, range, and seed.
- **Visualization:** Built-in plotting for 1D/2D and slice viewer for 3D.

## Requirements

- Python 3.7+
- numpy
- matplotlib

Install dependencies with:
```sh
pip install numpy matplotlib
```

## Usage

Run the script directly to see example outputs:
```sh
python perlin.py
```

### Example: 1D Perlin Noise

```python
from perlin import PerlinNoise1D

perlin = PerlinNoise1D(length=1000, octaves=5, persistence=0.53, ranges=[0, 5], seed=127.1)
noise = perlin.get_noise()
PerlinNoise1D.plot_noise(noise)
```

### Example: 2D Perlin Noise

```python
from perlin import PerlinNoise2D

perlin2d = PerlinNoise2D(width=100, height=100, octaves=6, persistence=0.5, ranges=[-1, 1])
noise2d = perlin2d.get_noise()
PerlinNoise2D.plot_noise(noise2d)
```

### Example: 3D Perlin Noise

```python
from perlin import PerlinNoise3D

perlin3d = PerlinNoise3D(width=64, height=64, depth=32, octaves=4)
noise3d = perlin3d.get_noise()
PerlinNoise3D.view_slices(noise3d, axis='z', delay=0.05)
```

## File Overview

- `perlin.py` — All Perlin noise classes and visualization functions.

## License

MIT License

---

*Inspired by Ken Perlin’s original algorithm.*
