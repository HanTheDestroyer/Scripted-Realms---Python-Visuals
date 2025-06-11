#version 330 core

uniform float max_vel;

in float frag_velocity_mag; // velocity magnitude squared
out vec4 fragColor;

void main() {
    float max_vel_sq = max_vel * max_vel;
    float ratio = clamp(frag_velocity_mag / max_vel_sq, 0.0, 1.0);

    // Map ratio [0..1] to hue angle [0..360 degrees]
    float hue = ratio * 360.0;

    // Convert hue to RGB using HSV to RGB conversion (s=1,v=1)
    float c = 1.0;
    float x = c * (1.0 - abs(mod(hue / 60.0, 2.0) - 1.0));
    vec3 rgb;

    if (hue < 60.0) {
        rgb = vec3(c, x, 0.0);
    } else if (hue < 120.0) {
        rgb = vec3(x, c, 0.0);
    } else if (hue < 180.0) {
        rgb = vec3(0.0, c, x);
    } else if (hue < 240.0) {
        rgb = vec3(0.0, x, c);
    } else if (hue < 300.0) {
        rgb = vec3(x, 0.0, c);
    } else {
        rgb = vec3(c, 0.0, x);
    }

    fragColor = vec4(rgb, 1.0);
}