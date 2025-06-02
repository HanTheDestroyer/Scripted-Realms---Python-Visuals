

from moderngl_window import WindowConfig
import moderngl
import cupy as cp
from particle import Particle
import sys


class Animation(WindowConfig):
    gl_version = (3, 3)
    title = 'Chladni Patterns Animation'
    resizable = False
    aspect_ratio = None
    window_size = (1280, 1280)
    vsync = True

    MAX_VELOCITY = 0.00125

    def __init__(self, **kwargs):
        # Inherit the parent attributes.
        super().__init__(**kwargs)
        # Enable the necessary OpenGL features.
        self.ctx.enable(moderngl.PROGRAM_POINT_SIZE)
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE

        # Create a particle system using 100k particles.
        num_particles = 25000
        center_x  = cp.random.uniform(-1, 1, num_particles).astype('f4')
        center_y  = cp.random.uniform(-1, 1, num_particles).astype('f4')
        thickness = cp.zeros(num_particles, dtype='f4')
        radius    = cp.ones(num_particles, dtype='f4') * 0.0025
        velocity_x = cp.random.uniform(-self.MAX_VELOCITY, self.MAX_VELOCITY, num_particles).astype('f4')
        velocity_y = cp.random.uniform(-self.MAX_VELOCITY, self.MAX_VELOCITY, num_particles).astype('f4')

        self.particles = Particle(
            center_x=center_x,
            center_y=center_y,
            thickness=thickness,
            radius=radius,
            ctx=self.ctx,
            resolution=self.window_size,
            vertex_shader=r'C:/Users/han\Documents/Creative Coding/P04 - Chladni Patterns 2D/Shaders/particle.vert',
            fragment_shader=r'C:/Users/han\Documents/Creative Coding/P04 - Chladni Patterns 2D/Shaders/particle.frag',
            velocity_x=velocity_x,
            velocity_y=velocity_y
        )


    def on_render(self, time, frame_time):
        """Render the particles."""
        self.ctx.clear()
        self.particles.move()
        self.particles.update_buffers()
        self.particles.check_transition(time)
        self.particles.vao.render(moderngl.POINTS)


if __name__ == '__main__':
    # Run the animation.
    Animation.run()
    sys.exit()

