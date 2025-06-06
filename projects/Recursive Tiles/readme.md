# Recursive Tiles

Recursive Tiles is a generative art project that creates a fractal-like pattern by recursively subdividing a rectangle into a 3x3 grid of colored tiles. Each tile is drawn with a randomized pastel color, resulting in a vibrant, organic mosaic with a pink-yellowish palette.

## Features

- **Recursive Subdivision:** Each tile divides itself into a 3x3 grid of sub-tiles, continuing until a minimum size is reached.
- **Center-Based Positioning:** Tiles are positioned based on their center for symmetry.
- **Pastel Color Palette:** Uses a base RGBA color with randomized brightness for visual variety.
- **Customizable Depth:** Recursion depth is determined automatically by tile size.

## Example Output

![Recursive Tiles Example](recursive_tiles.png)

## Usage

1. **Install Dependencies**

   This project uses [CuPy](https://cupy.dev/) for fast array operations. Install with:

   ```sh
   pip install cupy
   ```

   Make sure you have a compatible CUDA environment for CuPy.

2. **Run the Script**

   ```sh
   python RecursiveTiles
   ```

   This will generate `recursive_tiles.png` in the project directory.

## File Structure

- `RecursiveTiles` – Main script containing the `Tile` class and drawing logic.
- `canvas.py` – Canvas class for managing the drawing surface and saving images.

## Customization

- **Tile Size:** Change the `size` variable in the `__main__` section.
- **Color Palette:** Adjust the RGBA tuple passed to the `Tile` constructor for different color themes.
- **Subdivision Grid:** The script currently uses a 3x3 grid; modify the logic for different patterns.

