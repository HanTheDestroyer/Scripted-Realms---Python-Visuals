from canvas import Canvas
import numpy as np
from circle import Circle
from time import time


class CirclePacking:
    def __init__(self, canvas=Canvas(2000, 2000)):
        self.canvas = canvas
        self.circles = []
        self.radii_set     = np.array([10, 20, 40, 60, 80, 140, 200, 300, 500], dtype=np.float32)
        self.radii_set = self.radii_set[::-1]
        self.thickness_set = np.array([0, 1, 2, 3, 4, 7, 10, 15, 20], dtype=np.float32)
        self.thickness_set = self.thickness_set[::-1] # Reverse the order for descending thickness
        self.color_set     = np.array([
                                    [255, 68 , 68 , 255],     # Vivid red
                                    [255, 153, 51 , 255],     # Orange
                                    [255, 255, 0  , 255],     # Bright yellow
                                    [0  , 255, 128, 255],     # Aqua green
                                    [0  , 204, 255, 255],     # Cyan
                                    [51 , 153, 255, 255],     # Sky blue
                                    [102, 102, 255, 255],     # Soft indigo
                                    [204, 102, 255, 255],     # Purple
                                    [255, 51 , 153, 255],     # Hot pink
                                    [255, 255, 255, 255],     # White
                            ], dtype=np.uint8)

    def generate_stamps(self):
        """
        Generate a random set of circles.
        """
        for counter in range(len(self.radii_set)):
            radius    = self.radii_set[counter]
            thickness = self.thickness_set[counter]
            stamp_set = []
            for color in self.color_set:
                circle = Circle(radius, color, thickness)
                circle.make_patch()
                stamp_set.append(circle)
            self.circles.append(stamp_set)
            print(f"Generated {len(stamp_set)} stamps for radius {radius} and thickness {thickness}")


        
    def pack_circles(self):
        """
        Packs circles onto the canvas using a random approach.
        """
        counter_limits = [5, 10, 20, 40, 80, 160, 320, 640, 1280]
        counter_limits = np.array(counter_limits, dtype=np.int32)
        counter_limits *= 10
        max_attempts_per_circle = 250  # You can adjust this

        for i in range(len(self.radii_set)):
            counter = 0
            attempts = 0
            while counter < counter_limits[i] and attempts < counter_limits[i] * max_attempts_per_circle:
                attempts += 1
                # Select Stamp Set.
                stamp_set = self.circles[i]
                # Select a random stamp from the set.
                stamp = np.random.choice(stamp_set)
                stamp = stamp.patch
                # Select the thickness and the radius of the circle.
                radius = self.radii_set[i]
                thickness = self.thickness_set[i]
                x = np.random.randint(radius + thickness, self.canvas.columns - radius - thickness)
                y = np.random.randint(radius + thickness, self.canvas.rows - radius - thickness)
                # Check if the circle can be placed at the position (x, y).
                can_place = True
                # Select the part of the canvas where the circle will be placed.
                side_length = stamp.shape[0]
                half = side_length // 2

                x_min = x - half
                x_max = x + half + 1
                y_min = y - half
                y_max = y + half + 1

                # Check bounds to avoid out-of-bounds errors
                if x_min < 0 or y_min < 0 or x_max > self.canvas.columns or y_max > self.canvas.rows:
                    can_place = False
                else:
                    canvas_part = self.canvas.grid[y_min:y_max, x_min:x_max]
                    if np.any(canvas_part[..., 3] > 0):
                        can_place = False
                if can_place:
                    self.canvas.grid[y_min:y_max, x_min:x_max] += stamp
                    counter += 1
            print(f"Placed {counter} circles of radius {self.radii_set[i]} (attempted {attempts} times)")



if __name__ == "__main__":
    start_time = time()
    circle_packing = CirclePacking()
    circle_packing.generate_stamps()
    circle_packing.pack_circles()
    circle_packing.canvas.save_image('packed_circles3.png')
    end_time = time()
    print(f"Circle packing completed in {end_time - start_time:.2f} seconds.")