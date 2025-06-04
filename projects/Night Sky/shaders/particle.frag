#version 330 core

uniform vec2 resolution;

in float frag_thickness;
in float frag_center_x;
in float frag_center_y;
in float frag_radius;

out vec4 fragColor;

void main() {
    vec2 frag_position = -1.0 + 2.0 * gl_FragCoord.xy / resolution;
    vec2 frag_center = vec2(frag_center_x, frag_center_y);

    float distance = length(frag_position - frag_center);
    float glow_radius = frag_radius + frag_thickness;

    if (distance > glow_radius) {
        discard;
    }

    // Calculate normalized distance from center [0.0 (center) .. 1.0 (edge of glow)]
    float norm_dist = distance / glow_radius;

    // Lightning color: bright white core fading to electric blue edges
    vec3 lightning_color = mix(vec3(0.7, 0.85, 1.0), vec3(0.1, 0.3, 0.9), norm_dist);

    // Alpha decays exponentially with distance for a sharp glow
    float alpha = exp(-5.0 * norm_dist * norm_dist);

    fragColor = vec4(lightning_color, alpha);
}
