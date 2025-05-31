

from PIL import Image
import cupy as np
from canvas import Canvas
import matplotlib
from time import time


class Clifford:
    A = -1.24458046630025  
    B = -1.25191834103316  
    C = -1.81590817030519  
    D = -1.90866735205054
    NUM_POINTS = 10000000
    WARMUP_ITERATIONS = 250
    ITERATIONS = 25

    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.x = np.random.uniform(-2, +2, self.NUM_POINTS).astype('f4')
        self.y = np.random.uniform(-2, +2, self.NUM_POINTS).astype('f4')

    def func1(self, x, y):
        return np.sin(self.A * y) + self.C * np.cos(self.A * x)
    
    def func2(self, x, y):
        return np.sin(self.B * x) + self.D * np.cos(self.B * y)

    def iterate(self):
        # Warmup iterations to stabilize the attractor.
        for _ in range(self.WARMUP_ITERATIONS):
            x_new = self.func1(self.x, self.y)
            y_new = self.func2(self.x, self.y)
            self.x, self.y = x_new, y_new
        
        # Store iterations for final rendering
        x = np.zeros((self.ITERATIONS, self.NUM_POINTS), dtype=np.float32)
        y = np.zeros((self.ITERATIONS, self.NUM_POINTS), dtype=np.float32)

        x[0], y[0] = self.x, self.y
        for t in range(1, self.ITERATIONS):
            x[t] = self.func1(x[t-1], y[t-1])
            y[t] = self.func2(x[t-1], y[t-1])
        
        self.x = x
        self.y = y

    def remap(self):
        x_flat = self.x.flatten()
        y_flat = self.y.flatten()
        x_min, x_max = np.min(x_flat), np.max(x_flat)
        y_min, y_max = np.min(y_flat), np.max(y_flat)

        self.x = (self.x - x_min) / (x_max - x_min) * (self.canvas.columns - 1)
        self.y = (self.y - y_min) / (y_max - y_min) * (self.canvas.rows - 1)

    def paint(self):
        x_all = self.x.flatten()
        y_all = self.y.flatten()
        y_all = self.canvas.rows - 1 - y_all  # flip y-axis for image coordinate system

        density, _, _ = np.histogram2d(
            y_all, x_all,
            bins=(self.canvas.rows, self.canvas.columns),
            range=[[0, self.canvas.rows], [0, self.canvas.columns]]
        )

        # Convert density to float before log for precision
        log_density = np.log(density + 1)
        max_log_density = np.max(log_density)
        if max_log_density == 0:
            max_log_density = 1
        normalized_log_density = log_density / max_log_density

        colormap = matplotlib.colormaps['inferno']
        rgba_image = (colormap(normalized_log_density.get()) * 255).astype(np.uint8)

        self.canvas.grid[:, :, :] = rgba_image
        name = 'clifford_attractor.png' + f'{self.A}_{self.B}_{self.C}_{self.D}.png'
        self.canvas.save_image(name)


if __name__ == '__main__':
    start = time()
    canvas = Canvas(2000, 2000)
    clifford = Clifford(canvas)
    clifford.iterate()
    clifford.remap()
    clifford.paint()
    print("Clifford attractor image saved.")
    end = time()
    print(f"Execution time: {end - start:.2f} seconds")
    
