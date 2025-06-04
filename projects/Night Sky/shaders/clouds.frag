#version 330 core

in vec2 uv;
out vec4 fragColor;

uniform sampler2D noise_texture;

void main() {
    // Sample the noise texture
    float noise_value = texture(noise_texture, uv).r;

    // Map noise_value to cloud alpha or color as you wish
    float alpha = noise_value;

    // Output white clouds with variable transparency
    fragColor = vec4(vec3(1.0), alpha);
}