
#version 330 core

// Center and Color are normalized before passing to the shader.
layout(location = 0) in float in_center_x;
layout(location = 1) in float in_center_y;
layout(location = 6) in float in_thickness;
layout(location = 7) in float in_radius;
layout(location = 8) in float in_chladni_value;

uniform vec2 resolution;

out float frag_thickness;
out float frag_radius;
out float frag_center_x;
out float frag_center_y;
out float frag_chladni_value;

void main() {
    gl_Position = vec4(in_center_x, in_center_y, 0.0, 1.0);
    // Point-sprite diameter must be 2 x radius.
    gl_PointSize = in_radius * resolution.x;
    // Compile the color.
    frag_radius    = in_radius;
    frag_thickness = in_thickness;
    frag_center_x  = in_center_x;
    frag_center_y  = in_center_y;
    frag_chladni_value = in_chladni_value;
}
