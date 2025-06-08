#version 330 core

in float frag_velocity_mag;
out vec4 fragColor;

vec3 hsv2rgb(float h, float s, float v) {
    float c = v * s;
    float x = c * (1.0 - abs(mod(h * 6.0, 2.0) - 1.0));
    float m = v - c;
    vec3 rgb;

    if (0.0 <= h && h < 1.0/6.0) {
        rgb = vec3(c, x, 0.0);
    } else if (1.0/6.0 <= h && h < 2.0/6.0) {
        rgb = vec3(x, c, 0.0);
    } else if (2.0/6.0 <= h && h < 3.0/6.0) {
        rgb = vec3(0.0, c, x);
    } else if (3.0/6.0 <= h && h < 4.0/6.0) {
        rgb = vec3(0.0, x, c);
    } else if (4.0/6.0 <= h && h < 5.0/6.0) {
        rgb = vec3(x, 0.0, c);
    } else {
        rgb = vec3(c, 0.0, x);
    }

    return rgb + vec3(m);
}

void main() {
    float gain = 100000.0;
    float v = clamp(frag_velocity_mag * gain, 0.0, 1.0);

    // Full hue range from 0 to 1
    float hue = v;
    float saturation = 1.0;
    float value = 1.0;

    vec3 color = hsv2rgb(hue, saturation, value);
    fragColor = vec4(color, 1.0);
}
