import numpy as np
from canvas import Canvas


class Circle:
    """
    This class represents a circle with a specified radius and position.
    It can draw itself onto a canvas.
    """
    def __init__(self, radius, color, thickness=3):
        self.radius    = radius
        self.color     = color
        self.thickness = thickness
        # Generate a 2d image for the circle.
        self.side_length = int(2 * (self.radius + self.thickness)) + 1  # +1 to include the edge pixel
        self.patch = np.zeros((self.side_length, self.side_length, 4), dtype=np.uint8)
    
    def make_patch(self):
        """Makes a patch of the circle that can be stamped to canvas."""
        # Calculate the center of the patch.
        patch_center = (self.side_length // 2, self.side_length // 2)
        # Iterate over the bounding box of the circle.
        for y in range(self.side_length):
            for x in range(self.side_length):
                distance = np.sqrt((x - patch_center[0]) ** 2 + (y - patch_center[1]) ** 2)
                # Solid circle for thickness = 0.
                if self.thickness == 0:
                    if distance <= self.radius:
                        self.patch[y, x] = self.color
                # Hollow circle for thickness > 0.
                else:
                    if self.radius - self.thickness <= distance <= self.radius:
                        self.patch[y, x] = self.color









