

from moderngl_window import WindowConfig
import moderngl
import numpy as np
import sys
from particle import Particle
from time import sleep


class ColorSlices(WindowConfig):
    gl_version = (3, 3)
    title = 'Color Slices'
    resizable = False
    aspect_ratio = None
    window_size = (1280, 1280)
    vsync = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.ctx.enable(moderngl.BLEND)
        # self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA
        # Create a particle object that can hold multiple particles.
        num_particles_per_axis = 1280
        x = np.linspace(-1, 1, num_particles_per_axis, dtype='f4')
        y = np.linspace(-1, 1, num_particles_per_axis, dtype='f4')
        grid_x, grid_y = np.meshgrid(x, y)
        self.center_x = grid_x.ravel()
        self.center_y = grid_y.ravel()
        size     = 2 / num_particles_per_axis
        self.particles = Particle(
            center_x=self.center_x,
            center_y=self.center_y,
            size=size,
            ctx=self.ctx,
            resolution=self.window_size,
            vertex_shader=r'C:/Users/han/Documents/Creative Coding/P12 - Mandelbrot/shaders/particle.vert',
            fragment_shader=r'C:/Users/han/Documents/Creative Coding/P12 - Mandelbrot/shaders/particle.frag'
        )
        self.zoom_factor = 1.0
        self.wait_lock = True

    def on_render(self, time, frame_time):
        """Render the color slices."""
        self.ctx.clear()
        self.zoom_factor *= 0.999
        self.particles.update_buffers()
        self.particles.shader_program['zoom_factor'].value = self.zoom_factor
        self.particles.shader_program['mandelbrot_center_x'].value = 0.743643887037151
        self.particles.shader_program['mandelbrot_center_y'].value = 0.131825904205330
        self.particles.vao.render(moderngl.POINTS)
        if self.wait_lock:
            self.wait_lock = False
            sleep(4)

if __name__ == "__main__":
    # Run the application.
    ColorSlices.run()
    sys.exit(0)