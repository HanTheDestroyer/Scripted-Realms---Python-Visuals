

import cupy as np
from perlin import PerlinNoise2D as p2d
import moderngl


class Clouds:
    NUMBER_OF_2D_NOISE_SLICES = 1000
    def __init__(self, size, octaves, persistence, seed=127.1, ranges=[0, 1], ctx=None):
        self.size = size
        self.octaves = octaves
        self.persistence = persistence
        self.seed = seed
        self.ctx = ctx
        self.fragment_shader = r'C:/Users/han/Documents/Creative Coding/P06 - Night Sky/shaders/clouds.frag'
        self.vertex_shader = r'C:/Users/han/Documents/Creative Coding/P06 - Night Sky/shaders/clouds.vert'

        # Create a 2d Noise.
        starting_point = np.arange(0, self.NUMBER_OF_2D_NOISE_SLICES, dtype='f4') / 5000
        self.noise = []
        for t in range(self.NUMBER_OF_2D_NOISE_SLICES):
            noise = p2d(starting_point=[starting_point[t], 0], ranges=[0, 1], octaves=self.octaves, persistence=self.persistence, seed=self.seed)
            noise = noise.get_noise()
            self.noise.append(noise)
        self.noise = np.array(self.noise, dtype='f4')

        with open(self.vertex_shader) as f:
            self.vertex_shader = f.read()
        with open(self.fragment_shader) as f:
            self.fragment_shader = f.read()
        self.shader_program = self.ctx.program(vertex_shader=self.vertex_shader,
                                               fragment_shader=self.fragment_shader)
        
        vertices = np.array([
                            -1.0, -1.0,
                             1.0, -1.0,
                            -1.0,  1.0,
                            -1.0,  1.0,
                             1.0, -1.0,
                             1.0,  1.0,
                            ], dtype='f4')
        
        self.vbo = self.ctx.buffer(vertices.tobytes())
        self.vao = self.ctx.simple_vertex_array(self.shader_program, self.vbo, 'in_position')

    def render(self, time, frame_time):
        self.vao.render(moderngl.TRIANGLES)








if __name__ == '__main__':
    pass
        