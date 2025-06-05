
# Rect Packing with Triangular Squares

This project demonstrates a creative approach to packing squares—each rendered as four triangles with varying shades—onto a canvas using Python and NumPy. The packing is visualized and saved as an image, and the code calculates the packing percentage based on non-transparent pixels.

## Features

- Packs squares of different sizes onto a canvas without overlap.
- Each square is drawn using four triangles with gradient shading.
- Saves the result as a PNG image.
- Calculates and prints the packing percentage.

## Requirements

- Python 3.x
- numpy
- pillow

Install dependencies with:

```bash
pip install numpy pillow
```

## Usage

Run the main script:

```bash
python rect_packing.py
```

This will generate an output image and print the packing percentage.

## Example Output

Below is an example of the generated packing image:

![Example Packing](Outputs/image.png)

## File Structure

- `rect_packing.py` – Main script for packing and visualization.
- `canvas.py` – Canvas class for image creation and saving.
- `triangular_square.py` – Logic for drawing a square as four triangles.

## License

MIT License
