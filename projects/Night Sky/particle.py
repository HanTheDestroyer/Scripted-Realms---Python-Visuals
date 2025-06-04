

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

        self.cupy_the_values()
        # Load the shaders.
        self.shader_program = None
        self.generate_shader_program()
        # Reserve space for the values and create the buffers.
        self.num_circles         = len(self.center_x)
        self.vbo_center_x        = self.ctx.buffer(reserve=self.num_circles * 4)
        self.vbo_center_y        = self.ctx.buffer(reserve=self.num_circles * 4)
        self.vbo_thickness       = self.ctx.buffer(reserve=self.num_circles * 4)
        self.vbo_radius          = self.ctx.buffer(reserve=self.num_circles * 4)
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
                                        ])

    # noinspection PyUnresolvedReferences
    def update_buffers(self):
        """Update the buffers with the current values."""
        self.vbo_center_x.write(self.center_x.tobytes())
        self.vbo_center_y.write(self.center_y.tobytes())
        self.vbo_thickness.write(self.thickness.tobytes())
        self.vbo_radius.write(self.radius.tobytes())
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
        


if __name__ == "__main__":
    pass
