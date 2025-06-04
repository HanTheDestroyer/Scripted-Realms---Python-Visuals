

from moderngl_window import WindowConfig
import moderngl
import cupy as np
import sys
from clouds import Clouds
from particle import Particle


class NightSky(WindowConfig):
    gl_version = (3, 3)
    title = 'Night Sky Animation'
    resizable = False
    aspect_ratio = None
    window_size = (1280, 1280)
    vsync = True

    def __init__(self, **kwargs):
        # Inherit the parent attributes.
        super().__init__(**kwargs)
        # Enable the necessary OpenGL features.
        self.ctx.enable(moderngl.PROGRAM_POINT_SIZE)
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = moderngl.SRC_ALPHA, moderngl.ONE
        # Create a cloud object.
        self.clouds = Clouds(size=self.window_size[0], octaves=7, persistence=0.6, seed=127.1, ranges=[0, 1], ctx=self.ctx)
        self.counter = 0
        # Create a particle object.
        num_particles = 1
        center_x  = np.random.uniform(-1, 1, num_particles).astype('f4')
        center_y  = np.random.uniform(-1, 1, num_particles).astype('f4')
        thickness = np.zeros(num_particles, dtype='f4')
        radius    = np.random.uniform(0.02, 0.03, num_particles).astype('f4')
        self.particles = Particle(
            center_x=center_x,
            center_y=center_y,
            thickness=thickness,
            radius=radius,
            ctx=self.ctx,
            resolution=self.window_size,
            vertex_shader=r'C:/Users/han/Documents/Creative Coding/P06 - Night Sky/shaders/particle.vert',
            fragment_shader=r'C:/Users/han/Documents/Creative Coding/P06 - Night Sky/shaders/particle.frag'
        )
        


    def on_render(self, time, frame_time):
        self.ctx.clear()
        # Select the noise slice
        noise_slice = self.clouds.noise[self.counter % self.clouds.NUMBER_OF_2D_NOISE_SLICES]
        self.counter += 1
        # Convert to CPU array
        noise_cpu = noise_slice.get() if hasattr(noise_slice, 'get') else noise_slice
        # Create or update the texture
        noise_texture = self.ctx.texture(
            noise_cpu.shape[::-1],  # (width, height)
            1,                      # grayscale
            data=noise_cpu.tobytes(),
            dtype='f4'              # Specify float32 data type explicitly
        )
        # Bind texture to slot 0 (or whichever your shader expects)
        noise_texture.use(location=0)
        # Render call here
        self.clouds.vao.render()
        self.particles.radius = (self.particles.radius + 0.001) % 0.25
        self.particles.update_buffers()
        self.particles.vao.render(mode=moderngl.POINTS)






if __name__ == '__main__':
    # Run the animation.
    NightSky.run()
    sys.exit()

