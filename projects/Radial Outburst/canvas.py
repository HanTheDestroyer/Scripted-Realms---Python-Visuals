

from PIL import Image
import numpy as np
import os


class Canvas:
    """
    This class creates a blank canvas of specified dimensions.
    The canvas is initialized with a black background and can be saved as an image.
    """
    def __init__(self, rows, columns):
        # Create a blank canvas with the specified width and height
        self.columns = columns
        self.rows    = rows
        self.grid    = np.zeros((self.rows, self.columns, 4), dtype=np.uint8)  # Initialize a black canvas

    def save_image(self, filename='output.png'):
        os.makedirs('Outputs', exist_ok=True)
        img = Image.fromarray(self.grid)
        img.save('Outputs/' + filename)

