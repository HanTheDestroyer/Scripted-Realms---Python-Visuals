#version 330 core

in vec2 in_position;
out vec2 uv;

void main() {
    uv = in_position * 0.5 + 0.5;  // Convert from [-1,1] to [0,1] for texture coords
    gl_Position = vec4(in_position, 0.0, 1.0);
}