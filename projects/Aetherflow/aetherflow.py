

import cupy as cp
from moderngl_window import WindowConfig
import moderngl
from particle import Particle
from perlin import PerlinNoise2D
import sys


class Aetherflow(WindowConfig):
    gl_version = (3, 3)
    title = 'Aetherflow'
    resizable = False
    aspect_ratio = None
    window_size = (1280, 1280)
    vsync = True


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Enable required OpenGL features.
        self.ctx.enable(moderngl.PROGRAM_POINT_SIZE)
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE

        # Create a Particle System.
        num_particles = 100000
        center_x = cp.random.uniform(-1, 1, num_particles).astype('f4')
        center_y = cp.random.uniform(-1, 1, num_particles).astype('f4')
        size     = 1
        velocity_x = cp.random.uniform(-0.00125, 0.00125, num_particles).astype('f4')
        velocity_y = cp.random.uniform(-0.00125, 0.00125, num_particles).astype('f4')
        self.particles = Particle(
            center_x=center_x,
            center_y=center_y,
            size=size,
            ctx=self.ctx,
            resolution=self.window_size,
            vertex_shader=r'C:/Users/han/Documents/Creative Coding/P13 - Aetherflow/shaders/particle.vert',
            fragment_shader=r'C:/Users/han/Documents/Creative Coding/P13 - Aetherflow/shaders/particle.frag',
            velocity_x=velocity_x,
            velocity_y=velocity_y
        )

        self.perlin_noise = PerlinNoise2D(1280, 1280, seed=42, persistence=0.54, octaves=8, ranges=[0, 1]).get_noise()
        self.perlin_noise = cp.array(self.perlin_noise, dtype='f4') / 2


    def on_render(self, time, frame_time):
        """Render the particles."""
        # Compute the curl of the Perlin noise field.
        self.particles.velocity_x, self.particles.velocity_y = self.compute_curl(self.perlin_noise, self.particles.center_x, self.particles.center_y)
        self.particles.move()
        # Update the buffers with the new values.
        self.particles.update_buffers()
        self.particles.vao.render(moderngl.POINTS)


    def compute_curl(self, noise, x, y):
        h, w = noise.shape
        ix = ((x + 1) * 0.5 * (w - 1)).astype('i4')
        iy = ((y + 1) * 0.5 * (h - 1)).astype('i4')

        ix_plus = cp.clip(ix + 1, 0, w - 1)
        ix_minus = cp.clip(ix - 1, 0, w - 1)
        iy_plus = cp.clip(iy + 1, 0, h - 1)
        iy_minus = cp.clip(iy - 1, 0, h - 1)

        dFdx = (noise[iy, ix_plus] - noise[iy, ix_minus]) / 2  # 2 here corresponds to one pixel spacing
        dFdy = (noise[iy_plus, ix] - noise[iy_minus, ix]) / 2

        return dFdy, -dFdx









        

if __name__ == '__main__':
    Aetherflow.run()
    sys.exit()