

# Start with imports.
import cupy as cp


class Particle:
    n = 1
    m = 3
    L = 1
    threshold = 0.01
    transition_duration = 1
    pattern_duration = 5
    def __init__(self, **configs):
        # Define the default values for the properties or use the provided values.
        self.center_x        = configs.get('center_x', [0])
        self.center_y        = configs.get('center_y', [0])
        self.resolution      = configs.get('resolution', [1280.0, 1280.0])
        self.thickness       = configs.get('thickness', [0])
        self.radius          = configs.get('radius', [50])
        self.ctx             = configs.get('ctx', None)
        self.vertex_shader   = configs.get('vertex_shader', 'Shaders/circle.vert')
        self.fragment_shader = configs.get('fragment_shader', 'Shaders/circle.frag')
        self.velocity_x      = configs.get('velocity_x', [0])
        self.velocity_y      = configs.get('velocity_y', [0])
        self.chladni_value   = cp.zeros(len(self.center_x), dtype='f4')

        self.cupy_the_values()
        self.chladni_func()
        # Load the shaders.
        self.shader_program = None
        self.generate_shader_program()
        # Reserve space for the values and create the buffers.
        self.num_circles         = len(self.center_x)
        self.vbo_center_x        = self.ctx.buffer(reserve=self.num_circles * 4)
        self.vbo_center_y        = self.ctx.buffer(reserve=self.num_circles * 4)
        self.vbo_thickness       = self.ctx.buffer(reserve=self.num_circles * 4)
        self.vbo_radius          = self.ctx.buffer(reserve=self.num_circles * 4)
        self.vbo_chladni_value   = self.ctx.buffer(reserve=self.num_circles * 4)
        self.update_buffers()
        # Create the vertex array object.
        self.vao = None
        self.generate_vao()

    def generate_vao(self):
        """Creates VAO object."""
        self.vao = self.ctx.vertex_array(self.shader_program,
                                           [(self.vbo_center_x,      '1f', 'in_center_x'),
                                            (self.vbo_center_y,      '1f', 'in_center_y'),
                                            (self.vbo_thickness,     '1f', 'in_thickness'),
                                            (self.vbo_radius,        '1f', 'in_radius'),
                                            (self.vbo_chladni_value, '1f', 'in_chladni_value')])

    # noinspection PyUnresolvedReferences
    def update_buffers(self):
        """Update the buffers with the current values."""
        self.vbo_center_x.write(self.center_x.tobytes())
        self.vbo_center_y.write(self.center_y.tobytes())
        self.vbo_thickness.write(self.thickness.tobytes())
        self.vbo_radius.write(self.radius.tobytes())
        self.vbo_chladni_value.write(self.chladni_value.tobytes())
        self.shader_program['resolution'].value = self.resolution

    def generate_shader_program(self):
        """Load the shaders from the specified files and generates the shader program."""
        # Load the shaders.
        with open(self.vertex_shader) as f:
            self.vertex_shader = f.read()
        with open(self.fragment_shader) as f:
            self.fragment_shader = f.read()        # Create the shader program.
        self.shader_program = self.ctx.program(vertex_shader=self.vertex_shader,
                                               fragment_shader=self.fragment_shader)

    def cupy_the_values(self):
        """Convert all values to cupy arrays with dtype 'f4'."""
        self.center_x     = cp.array(self.center_x,   dtype='f4')
        self.center_y     = cp.array(self.center_y,   dtype='f4')
        self.resolution   = cp.array(self.resolution, dtype='f4')
        self.thickness    = cp.array(self.thickness,  dtype='f4')
        self.radius       = cp.array(self.radius,     dtype='f4')
        self.velocity_x   = cp.array(self.velocity_x, dtype='f4')
        self.velocity_y   = cp.array(self.velocity_y, dtype='f4')

    def move(self):
        """Move the particles based on their velocity."""
        self.center_x += self.velocity_x
        self.center_y += self.velocity_y
        # Particles will appear on the opposite side of the screen if they go out of bounds.
        mask_left   = self.center_x < -1
        mask_right  = self.center_x > +1
        mask_top    = self.center_y > +1
        mask_bottom = self.center_y < -1
        self.center_x[mask_left]   = +1
        self.center_x[mask_right]  = -1
        self.center_y[mask_top]    = -1
        self.center_y[mask_bottom] = +1

    def chladni_func(self):
        """Calculate the Chladni pattern using cosine func."""
        product_1 = cp.cos(self.n * cp.pi * self.center_x / self.L)
        product_2 = cp.cos(self.m * cp.pi * self.center_y / self.L)
        product_3 = cp.cos(self.m * cp.pi * self.center_x / self.L)
        product_4 = cp.cos(self.n * cp.pi * self.center_y / self.L)
        self.chladni_value = cp.abs(product_1 * product_2 - product_3 * product_4).astype('f4')
        mask = self.chladni_value < self.threshold
        self.velocity_x[mask] = 0
        self.velocity_y[mask] = 0

    def check_transition(self, time):
        """Check if the transition should happen based on the time."""
        if time % self.pattern_duration < self.transition_duration:
            # Transition to the next pattern.
            self.n = cp.random.uniform(1, 5)
            self.m = cp.random.uniform(1, 5)
            self.chladni_value *= 0
            self.velocity_x = cp.random.uniform(-0.00125, 0.00125, len(self.center_x)).astype('f4')
            self.velocity_y = cp.random.uniform(-0.00125, 0.00125, len(self.center_y)).astype('f4')
        else:
            self.chladni_func()

        


if __name__ == "__main__":
    pass
