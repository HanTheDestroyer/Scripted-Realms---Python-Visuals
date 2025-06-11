

import cupy as cp
from moderngl_window import WindowConfig
import moderngl
from particle import Particle
from perlin import PerlinNoise2D
import sys


class EtherFlow(WindowConfig):
    gl_version = (3, 3)
    title = 'EtherFlow'
    resizable = True
    aspect_ratio = None
    window_size = (1280, 1280)
    vsync = False

    max_velocity = 0.00150
    width = window_size[0]
    height = window_size[1]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Enable required OpenGL features.
        self.ctx.enable(moderngl.PROGRAM_POINT_SIZE)
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE

        # Create a Particle System.
        num_particles = 1000000
        center_x = cp.random.uniform(-1, 1, num_particles).astype('f4')
        center_y = cp.random.uniform(-1, 1, num_particles).astype('f4')
        size     = 1
        velocity_x = cp.random.uniform(-self.max_velocity, self.max_velocity, num_particles).astype('f4') * 0
        velocity_y = cp.random.uniform(-self.max_velocity, self.max_velocity, num_particles).astype('f4') * 0
        self.particles = Particle(
            center_x=center_x,
            center_y=center_y,
            size=size,
            ctx=self.ctx,
            resolution=self.window_size,
            vertex_shader=r'C:/Users/han/Documents/Creative Coding/P14 - Etherflow/shaders/particle.vert',
            fragment_shader=r'C:/Users/han/Documents/Creative Coding/P14 - Etherflow/shaders/particle.frag',
            velocity_x=velocity_x,
            velocity_y=velocity_y
        )

        self.a = PerlinNoise2D(self.width, self.height, seed=517.1, persistence=0.84, octaves=8, ranges=[-cp.pi, cp.pi]).get_noise()
        self.a = cp.array(self.a, dtype='f4') # Convert it to CuPy Array.
        self.b = PerlinNoise2D(self.width, self.height, seed=-23.5, persistence=0.84, octaves=8, ranges=[-cp.pi, cp.pi]).get_noise()
        self.b = cp.array(self.b, dtype='f4')

    def on_render(self, time, frame_time):
        """Render the particles."""
        # Dual Noise Trick for waves.
        C = cp.angle(cp.exp(1j * self.a) - cp.exp(1j * self.b))        # This C value is between 0 and 2pi. 
        sinC = cp.sin(C)
        cosC = cp.cos(C)
        x_indices = self.particles.center_x * 640 + 640
        y_indices = self.particles.center_y * 640 + 640
        x_indices = cp.clip(x_indices.astype(int), 0, self.a.shape[1] - 1)
        y_indices = cp.clip(y_indices.astype(int), 0, self.a.shape[0] - 1)
        mean_x = cp.mean(cp.cos(C))
        mean_y = cp.mean(cp.sin(C))
        print("Mean Field Direction:", float(mean_x), float(mean_y))
        self.particles.velocity_x += cosC[y_indices, x_indices] * 1e-6
        self.particles.velocity_y += sinC[y_indices, x_indices] * 1e-6


        self.particles.velocity_x = cp.clip(self.particles.velocity_x, -self.max_velocity, self.max_velocity)
        self.particles.velocity_y = cp.clip(self.particles.velocity_y, -self.max_velocity, self.max_velocity)

        self.particles.shader_program['max_vel'].value = self.max_velocity
        self.particles.move()
        # Update the buffers with the new values.
        # self.ctx.clear()
        self.particles.update_buffers()
        self.particles.vao.render(moderngl.POINTS)

        

if __name__ == '__main__':
    EtherFlow.run()
    sys.exit()