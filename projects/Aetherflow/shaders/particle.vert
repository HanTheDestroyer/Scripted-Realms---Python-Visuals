
#version 330 core

// Center and Color are normalized before passing to the shader.
layout(location = 0) in float in_center_x;
layout(location = 1) in float in_center_y;
layout(location = 2) in float in_velocity_mag;

uniform vec2 resolution;
uniform float size;

out float frag_velocity_mag;


void main() {
    gl_Position = vec4(in_center_x, in_center_y, 0.0, 1.0);
    gl_PointSize = size;
    frag_velocity_mag = in_velocity_mag;
}
