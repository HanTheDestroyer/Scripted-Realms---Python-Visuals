
#version 330 core

// Center and Color are normalized before passing to the shader.
layout(location = 0) in float in_center_x;
layout(location = 1) in float in_center_y;

uniform vec2 resolution;

out vec4 base_color;

void main() {
    gl_Position = vec4(in_center_x, in_center_y, 0.0, 1.0);
    // Compile the color.
    base_color = vec4(1.0, 1.0, 0.0, 1.0);
}
