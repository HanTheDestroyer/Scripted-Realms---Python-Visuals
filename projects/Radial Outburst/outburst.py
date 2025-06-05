

import cupy as cp
import numpy as np
from canvas import Canvas
from perlin import PerlinNoise2D, PerlinNoise1D


class RadialOutburst:
    """This class creates a radial outburst effect on a canvas using Perlin noise."""   
    def __init__(self):
        # First, create a canvas.
        self.canvas = Canvas(2000, 2000)
        
    def draw_star(self):        
        star_center = (1000, 1000)
        star_radius = 200
        x_min = star_center[0] - star_radius
        x_max = star_center[0] + star_radius
        y_min = star_center[1] - star_radius
        y_max = star_center[1] + star_radius
        perlin_noise = PerlinNoise2D(400, 400, seed=42, ranges=[0, 1], persistence=0.9, octaves=12)
        perlin_noise = perlin_noise.get_noise()
        perlin_noise = cp.clip(perlin_noise, 0, 1)  # Ensure noise values are between 0 and 1
        # Iterate over the pixels in the canvas.
        for y in range(y_min, y_max):
            for x in range(x_min, x_max):
                fragment_position = np.array([x, y], dtype=np.float32)
                # Calculate the distance from the star center.
                distance = np.linalg.norm(fragment_position - star_center)
                # If the distance is less than the star radius, set the pixel to a bright orange/red color.
                if distance < star_radius:
                    # Get a color using perlin noise.
                    px = x - x_min
                    py = y - y_min
                    noise = perlin_noise[py, px]
                    # Use this noise to create a color value.
                    red   = int(200 + 55 * noise)    # 200 to 255
                    green = int(50 + 130 * noise)    # 50 to 180
                    blue  = 0
                    alpha = 255
                    self.canvas.grid[y, x] = [red, green, blue, alpha]

    def draw_rays(self):
        star_center = (1000, 1000)
        star_radius = 200
        num_rays = 1000
        ray_length = 850
        ray_base_thickness = 3
        ray_tip_thickness = 1

        first_ray = np.array([1, 0], dtype=np.float32)  # Start with a ray pointing to the right.
        angle_increment = 2 * np.pi / num_rays
        ray_length_factor = PerlinNoise1D(num_rays, seed=42, ranges=[0, 1], persistence=0.9, octaves=12).get_noise()

        for i in range(num_rays):
            angle = i * angle_increment
            rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                        [np.sin(angle),  np.cos(angle)]])
            ray_direction = rotation_matrix @ first_ray
            ray_direction *= ray_length * ray_length_factor[i]
            ray_tip = star_center + ray_direction
            ray_base = star_center
            # Draw the ray from the base to the tip.
            x_max = int(max(ray_base[0], ray_tip[0]))
            x_min = int(min(ray_base[0], ray_tip[0]))
            y_max = int(max(ray_base[1], ray_tip[1]))
            y_min = int(min(ray_base[1], ray_tip[1]))
            print(f"Drawing ray {i + 1}/{num_rays} from {ray_base} to {ray_tip}")
            for y in range(y_min, y_max):
                for x in range(x_min, x_max):
                    fragment_position = np.array([x, y], dtype=np.float32)
                    # Calculate the distance from the ray base to the fragment position.
                    distance_to_base = np.linalg.norm(fragment_position - ray_base)
                    # Calculate the distance from the ray direction vector.
                    ab = ray_tip - ray_base
                    ap = fragment_position - ray_base
                    ab_ap = np.dot(ab, ap) / np.dot(ab, ab)
                    thickness = ray_base_thickness * (1 - ab_ap**3) + ray_tip_thickness * ab_ap**3

                    if 0 <= ab_ap <= 1:
                        projection_endpoint = ray_base + ab_ap * ab
                        distance_to_ray = np.linalg.norm(fragment_position - projection_endpoint)
                        if distance_to_ray < thickness:
                            # Set the pixel to a bright orange/red color.
                            t = ab_ap
                            red   = int(255 * (1 - t) + 255 * t)      # Keep at 255 for both base and tip
                            green = int(180 * (1 - t) * np.random.uniform(0.8, 1) + 120 * t)      # 180 at base, 120 at tip (warmer yellow/orange)
                            blue  = int(20 * (1 - t) + np.random.uniform(0, 1) * t)         # 20 at base, 0 at tip (almost no blue)
                            alpha = int(80 * (1 - t) + np.random.randint(0, 6) * t)         # Lower alpha for softer rays
                            self.canvas.grid[y, x] = [red, green, blue, alpha]











if __name__ == "__main__":
    # Create an instance of the RadialOutburst class.
    radial_outburst = RadialOutburst()
    radial_outburst.draw_rays()
    radial_outburst.draw_star()
    # Save the canvas as an image.
    radial_outburst.canvas.save_image('radial_outburst.png')
    print("Radial outburst effect created and saved as 'radial_outburst.png'.")

                    


