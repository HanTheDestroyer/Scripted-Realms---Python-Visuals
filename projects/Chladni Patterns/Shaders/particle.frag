// Fragment Shader start.
#version 330 core

// Uniforms.
uniform vec2 resolution;

// Inputs.
in float frag_thickness;
in float frag_center_x;
in float frag_center_y;
in float frag_radius;
in float frag_chladni_value;

// Output.
out vec4 fragColor;

void main() {
    // Convert from window coords to normalized [-1,1] space
    vec2 frag_position = -1.0 + 2.0 * gl_FragCoord.xy / resolution;
    vec2 frag_center = vec2(frag_center_x, frag_center_y);
    
    vec4 frag_color = vec4(0.0, 0.0, 0.0, 1.0);
    frag_color.r = frag_chladni_value;
    frag_color.g = 1.0 - frag_chladni_value;
    frag_color.b = 0.5 + 0.5 * sin(6.2831 * frag_chladni_value);

    float d = length(frag_position - frag_center);

    if (frag_thickness == 0.0) {
        // Filled circle
        if (d <= frag_radius) {
            fragColor = frag_color;
        } else {
            discard;
        }
    } else {
        // Hollow circle
        float inner = frag_radius - frag_thickness;
        if (d >= inner && d <= frag_radius) {
            fragColor = frag_color;
        } else {
            discard;
        }
    }
}
