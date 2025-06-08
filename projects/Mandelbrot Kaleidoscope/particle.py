

# Start with imports.
import numpy as np


class Particle:
    def __init__(self, **configs):
        # Define the default values for the properties or use the provided values.
        self.center_x        = configs.get('center_x', [0])
        self.center_y        = configs.get('center_y', [0])
        self.size            = configs.get('size', [0.01])
        self.resolution      = configs.get('resolution', [1280.0, 1280.0])
        self.ctx             = configs.get('ctx', None)
        self.vertex_shader   = configs.get('vertex_shader', 'Shaders/circle.vert')
        self.fragment_shader = configs.get('fragment_shader', 'Shaders/circle.frag')
        # NumPy the arrays.
        self.center_x     = np.array(self.center_x,   dtype='f4')
        self.center_y     = np.array(self.center_y,   dtype='f4')
        self.resolution   = np.array(self.resolution, dtype='f4')
        # Create a shader program.
        with open(self.vertex_shader) as f:
            self.vertex_shader = f.read()
        with open(self.fragment_shader) as f:
            self.fragment_shader = f.read()
        self.shader_program = self.ctx.program(vertex_shader=self.vertex_shader, fragment_shader=self.fragment_shader)
        # Reserve space for the values and create the buffers.
        self.num_circles         = len(self.center_x)
        self.vbo_center_x        = self.ctx.buffer(reserve=self.num_circles * 4)
        self.vbo_center_y        = self.ctx.buffer(reserve=self.num_circles * 4)
        # Update the buffers with the initial values once.
        self.update_buffers()
        # Create the vertex array object.
        self.vao = self.ctx.vertex_array(self.shader_program,
                                           [(self.vbo_center_x,      '1f', 'in_center_x'),
                                            (self.vbo_center_y,      '1f', 'in_center_y')])
        self.zoom_factor = 1.0

    # noinspection PyUnresolvedReferences
    def update_buffers(self):
        """Update the buffers with the current values."""
        self.vbo_center_x.write(self.center_x.tobytes())
        self.vbo_center_y.write(self.center_y.tobytes())
        self.shader_program['resolution'].value = self.resolution        # self.shader_program['zoom_factor'].value = self.zoom_factor



if __name__ == "__main__":
    pass
