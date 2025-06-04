import numpy as np


class PerlinNoise1D:
    def __init__(self,
                 length          = 1000,
                 octaves         = 5,
                 persistence     = 0.53,
                 ranges          = [-1, 1],
                 seed            = 127.1,
                 starting_point  = 0,
                 increment       = 0.001,
                 freq_multiplier = 2,
                 starting_freq   = 1):
        self.length          = np.float32(length)
        self.octaves         = np.float32(octaves)
        self.persistence     = np.float32(persistence)
        self.ranges          = np.array(ranges, dtype='f4')
        self.seed            = np.float32(seed)
        self.starting_point  = np.float32(starting_point)
        self.increment       = np.float32(increment)
        self.freq_multiplier = np.float32(freq_multiplier)
        self.starting_freq   = np.float32(starting_freq)
        self.numbers         = np.linspace(self.starting_point,
                                           self.starting_point + self.length * self.increment,
                                           int(self.length), dtype='f4')

    def gradient(self, val):
        x = np.sin(val * self.seed) * 43758.5453
        # Remap [0,1] → [-1,1]
        return (x - np.floor(x)) * 2.0 - 1.0 
    
    @staticmethod
    def fade(t):
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    def perlin(self, x):
        # Calculate the floor and ceil values.
        x_floor = np.floor(x)
        x_ceil  = x_floor + 1
        # Calculate the gradient values for floor and ceil.
        gradient_floor = self.gradient(x_floor)
        gradient_ceil  = self.gradient(x_ceil)
        # Calculate the distance values for the floor and ceil.
        dist_floor = x - x_floor
        dist_ceil  = x - x_ceil
        # Calculate the fade distance.
        fade_distance = self.fade(dist_floor)
        # Calculate the dot products for floor and ceil.
        dot_product_floor = gradient_floor * dist_floor
        dot_product_ceil  = gradient_ceil * dist_ceil
        # Interpolate between the two dot products.
        return dot_product_floor + fade_distance * (dot_product_ceil - dot_product_floor)
    
    def get_noise(self):
        total = np.zeros(int(self.length), dtype='f4')
        amplitude = 1.0
        frequency = self.starting_freq
        
        for _ in range(int(self.octaves)):
            total     += self.perlin(self.numbers * frequency) * amplitude
            amplitude *= self.persistence
            frequency *= self.freq_multiplier

        # Normalize the total to the range [-1, 1]
        total = (total - np.min(total)) / (np.max(total) - np.min(total)) * 2 - 1

        # Remap the values to the desired range
        return self.ranges[0] + (self.ranges[1] - self.ranges[0]) * (total + 1) / 2
    

    @staticmethod
    def plot_noise(noise):
        # Plot the Perlin noise
        import matplotlib.pyplot as plt
        # perlin_noise_values = np.random.uniform(0, 5, 1000)
        plt.plot(perlin.numbers, noise)
        plt.title("1D Perlin Noise")
        plt.xlabel("Index")
        plt.ylabel("Noise Value")
        plt.grid(True)
        plt.show()

    

class PerlinNoise2D:
    def __init__(self,
                 width = 1000,
                 height = 1000,
                 octaves = 5,
                 persistence = 0.53,
                 ranges = [-1, 1],
                 seed = 127.1,
                 starting_point = [0, 0],
                 increment = 0.001,
                 freq_multiplier = 2,
                 starting_freq = 1):
        self.width  = np.linspace(starting_point[0],
                                  starting_point[0] + width * increment,
                                  int(width), dtype='f4')
        self.height = np.linspace(starting_point[1],
                                  starting_point[1] + height * increment,
                                  int(height), dtype='f4')
        self.octaves         = np.float32(octaves)
        self.persistence     = np.float32(persistence)
        self.ranges          = np.array(ranges, dtype='f4')
        self.seed            = np.float32(seed)
        self.starting_freq   = np.float32(starting_freq)
        self.freq_multiplier = np.float32(freq_multiplier)
        self.final_value     = np.zeros((int(height), int(width)), dtype='f4')
        # Use 'ij' indexing to get (height, width) shape
        self.x_coord, self.y_coord = np.meshgrid(self.width, self.height, indexing='xy')

    def fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    def gradient(self, x, y):
        # Generate a pseudo-random gradient based on the coordinates and seed
        angle = (np.sin(x * 12.9898 + y * 78.233 + self.seed) * 43758.5453) % (2 * np.pi)
        self.grad_x = np.cos(angle)
        self.grad_y = np.sin(angle)

    def perlin(self, x, y):
        # Get the boundary box.
        x_floor = np.floor(x)
        x_ceil  = x_floor + 1
        y_floor = np.floor(y)
        y_ceil  = y_floor + 1

        # Calculate the gradient values for floor and ceil.
        # TOP LEFT
        self.gradient(x_floor, y_floor)
        gradient_x_TL = self.grad_x
        gradient_y_TL = self.grad_y
        # TOP RIGHT
        self.gradient(x_ceil, y_floor)
        gradient_x_TR = self.grad_x
        gradient_y_TR = self.grad_y
        # BOTTOM LEFT
        self.gradient(x_floor, y_ceil)
        gradient_x_BL = self.grad_x
        gradient_y_BL = self.grad_y
        # BOTTOM RIGHT
        self.gradient(x_ceil, y_ceil)
        gradient_x_BR = self.grad_x
        gradient_y_BR = self.grad_y

        # Calculate the distance values for the floor and ceil.
        dist_x_TL = x - x_floor
        dist_y_TL = y - y_floor
        dist_x_TR = x - x_ceil
        dist_y_TR = y - y_floor
        dist_x_BL = x - x_floor
        dist_y_BL = y - y_ceil
        dist_x_BR = x - x_ceil
        dist_y_BR = y - y_ceil

        # Dot Products - Element-Wise between gradient vectors and displacement vectors.
        dot_TL = gradient_x_TL * dist_x_TL + gradient_y_TL * dist_y_TL
        dot_TR = gradient_x_TR * dist_x_TR + gradient_y_TR * dist_y_TR
        dot_BL = gradient_x_BL * dist_x_BL + gradient_y_BL * dist_y_BL
        dot_BR = gradient_x_BR * dist_x_BR + gradient_y_BR * dist_y_BR

        # Fade the distances.
        fade_x = self.fade(dist_x_TL)
        fade_y = self.fade(dist_y_TL)

        # Interpolate Horizontally.
        interp_top    = dot_TL + fade_x * (dot_TR - dot_TL)
        interp_bottom = dot_BL + fade_x * (dot_BR - dot_BL)

        # Interpolate Vertically.
        self.final_value = interp_top + fade_y * (interp_bottom - interp_top)
        return self.final_value
    
    def get_noise(self):
        total = np.zeros(self.final_value.shape, dtype='f4')
        amplitude = 1.0
        frequency = self.starting_freq

        for _ in range(int(self.octaves)):
            x_scaled = self.x_coord * frequency
            y_scaled = self.y_coord * frequency
            # Calculate perlin noise for the octave over grid
            noise = self.perlin(x_scaled, y_scaled)
            total += noise * amplitude
            amplitude *= self.persistence
            frequency *= 2.0
        a, b = self.ranges
        total = a + (b - a) * (total + 1) / 2
        return total
    

    @staticmethod
    def plot_noise(noise):
        import matplotlib.pyplot as plt

        # 1D Slice Plot (like your current version)
        time_steps = noise.shape[0]
        plt.figure(figsize=(10, 6))
        for t in np.linspace(0, time_steps - 1, 10, dtype=int):
            plt.plot(np.linspace(0, 1, noise.shape[1]), noise[t], label=f"t={t}")
        plt.title("1D Perlin Noise Evolving Over Time (Slices from 2D Noise)")
        plt.xlabel("Space")
        plt.ylabel("Noise Value")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # 2D Noise Visualization
        plt.figure(figsize=(6, 6))
        plt.imshow(noise, cmap='viridis', origin='lower', interpolation='nearest')
        plt.colorbar(label='Noise Value')
        plt.title("2D Perlin Noise")
        plt.axis('off')  # Optional: turn off axes
        plt.tight_layout()
        plt.show()

class PerlinNoise3D:
    def __init__(self,
                 width = 128,
                 height = 128,
                 depth = 128,
                 octaves = 5,
                 persistence = 0.5,
                 ranges = [-1, 1],
                 seed = 127.1,
                 starting_point = [0, 0, 0],
                 increment = 0.01,
                 freq_multiplier = 2,
                 starting_freq = 1):
        self.width  = np.linspace(starting_point[0],
                                  starting_point[0] + width * increment,
                                  int(width), dtype='f4')
        self.height = np.linspace(starting_point[1],
                                  starting_point[1] + height * increment,
                                  int(height), dtype='f4')
        self.depth  = np.linspace(starting_point[2],
                                  starting_point[2] + depth * increment,
                                  int(depth), dtype='f4')
        self.octaves         = np.float32(octaves)
        self.persistence     = np.float32(persistence)
        self.ranges          = np.array(ranges, dtype='f4')
        self.seed            = np.float32(seed)
        self.starting_freq   = np.float32(starting_freq)
        self.freq_multiplier = np.float32(freq_multiplier)
        self.final_value     = np.zeros((int(depth), int(height), int(width)), dtype='f4')
        # Use 'ij' indexing to get (depth, height, width) shape
        self.z_coord, self.y_coord, self.x_coord = np.meshgrid(
            self.depth, self.height, self.width, indexing='ij'
        )

    def fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)
    
    def gradient(self, x, y, z):
        angle1 = (np.sin(x * 12.9898 + y * 78.233 + self.seed) * 43758.5453) % (2 * np.pi)
        angle2 = (np.sin(z * 45.164 + y * 23.927 + self.seed) * 23421.631) % (2 * np.pi)
        self.grad_x = np.cos(angle1) * np.sin(angle2)
        self.grad_y = np.sin(angle1) * np.sin(angle2)
        self.grad_z = np.cos(angle2)

    def perlin(self, x, y, z):
        x0 = np.floor(x)
        x1 = x0 + 1
        y0 = np.floor(y)
        y1 = y0 + 1
        z0 = np.floor(z)
        z1 = z0 + 1

        def dot_grid_gradient(ix, iy, iz, x, y, z):
            self.gradient(ix, iy, iz)
            dx = x - ix
            dy = y - iy
            dz = z - iz
            return self.grad_x * dx + self.grad_y * dy + self.grad_z * dz

        dx = x - x0
        dy = y - y0
        dz = z - z0

        u = self.fade(dx)
        v = self.fade(dy)
        w = self.fade(dz)

        n000 = dot_grid_gradient(x0, y0, z0, x, y, z)
        n100 = dot_grid_gradient(x1, y0, z0, x, y, z)
        n010 = dot_grid_gradient(x0, y1, z0, x, y, z)
        n110 = dot_grid_gradient(x1, y1, z0, x, y, z)
        n001 = dot_grid_gradient(x0, y0, z1, x, y, z)
        n101 = dot_grid_gradient(x1, y0, z1, x, y, z)
        n011 = dot_grid_gradient(x0, y1, z1, x, y, z)
        n111 = dot_grid_gradient(x1, y1, z1, x, y, z)

        nx00 = n000 + u * (n100 - n000)
        nx10 = n010 + u * (n110 - n010)
        nx01 = n001 + u * (n101 - n001)
        nx11 = n011 + u * (n111 - n011)

        nxy0 = nx00 + v * (nx10 - nx00)
        nxy1 = nx01 + v * (nx11 - nx01)

        self.final_value = nxy0 + w * (nxy1 - nxy0)
        return self.final_value

    def get_noise(self):
        total = np.zeros(self.final_value.shape, dtype='f4')
        amplitude = 1.0
        frequency = self.starting_freq

        for _ in range(int(self.octaves)):
            x_scaled = self.x_coord * frequency
            y_scaled = self.y_coord * frequency
            z_scaled = self.z_coord * frequency
            noise = self.perlin(x_scaled, y_scaled, z_scaled)
            total += noise * amplitude
            amplitude *= self.persistence
            frequency *= self.freq_multiplier

        a, b = self.ranges
        total = a + (b - a) * (total + 1) / 2
        return total
        
    @staticmethod
    def view_slices(noise, axis='z', delay=0.03):
        import matplotlib.pyplot as plt

        # Ensure valid axis
        if axis not in ['x', 'y', 'z']:
            raise ValueError("Axis must be one of: 'x', 'y', or 'z'.")

        plt.ion()
        fig, ax = plt.subplots()

        if axis == 'z':
            total_slices = noise.shape[0]
            img = ax.imshow(noise[0], cmap='viridis', vmin=noise.min(), vmax=noise.max())
        elif axis == 'y':
            total_slices = noise.shape[1]
            img = ax.imshow(noise[:, 0, :], cmap='viridis', vmin=noise.min(), vmax=noise.max())
        elif axis == 'x':
            total_slices = noise.shape[2]
            img = ax.imshow(noise[:, :, 0], cmap='viridis', vmin=noise.min(), vmax=noise.max())

        try:
            while True:
                for i in range(total_slices):
                    if axis == 'z':
                        img.set_data(noise[i])
                    elif axis == 'y':
                        img.set_data(noise[:, i, :])
                    elif axis == 'x':
                        img.set_data(noise[:, :, i])
                    ax.set_title(f"{axis.upper()} Slice {i}/{total_slices - 1}")
                    plt.draw()
                    plt.pause(delay)
        except KeyboardInterrupt:
            plt.ioff()
            plt.close()
    
    

if __name__ == '__main__':
    # Example usage
    perlin = PerlinNoise1D(length=1000, octaves=5, persistence=0.53, ranges=[0, 5], seed=127.1)
    perlin_noise_values = perlin.get_noise()
    PerlinNoise1D.plot_noise(perlin_noise_values)

    perlin = PerlinNoise2D(width=1000, height=100, octaves=8, persistence=0.63, seed=127.1, ranges=[-10, 1])
    perlin_noise_2d_values = perlin.get_noise()
    PerlinNoise2D.plot_noise(perlin_noise_2d_values)
    
    perlin = PerlinNoise3D(width=128, height=128, depth=100, octaves=5, persistence=0.5, seed=127.1, ranges=[-1, 1])
    perlin_noise_3d_values = perlin.get_noise()
    print(perlin_noise_3d_values.shape)  # Output the shape of the 3D noise array
    PerlinNoise3D.view_slices(perlin_noise_3d_values, axis='z', delay=0.01)