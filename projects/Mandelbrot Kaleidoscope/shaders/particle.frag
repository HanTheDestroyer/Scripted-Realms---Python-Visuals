#version 330 core

uniform vec2 resolution;
uniform float mandelbrot_center_x;
uniform float mandelbrot_center_y;
uniform float zoom_factor;

in vec4 base_color;
out vec4 fragColor;

vec2 remap(vec2 pos, float zoom, vec2 x_range, vec2 y_range) {
    float axis_len = 2.0;
    float zoomed_axis_len = axis_len * zoom;
    vec2 percentage = (pos + 1.0) / 2.0;
    return vec2(
        x_range.x + percentage.x * zoomed_axis_len,
        y_range.x + percentage.y * zoomed_axis_len
    );
}

vec2 apply_kaleidoscope(vec2 pos, float wedge_angle_deg) {
    float angle = degrees(atan(pos.y, pos.x));
    if (angle < 0.0) angle += 360.0;

    float wedge_index = floor(angle / wedge_angle_deg);
    float local_angle = angle - wedge_index * wedge_angle_deg;

    float rotated_angle = (int(wedge_index) % 2 == 0)
        ? local_angle
        : wedge_angle_deg - local_angle;

    float rad = length(pos);
    float final_angle = radians(rotated_angle);

    return vec2(cos(final_angle), sin(final_angle)) * rad;
}

int mandelbrot(vec2 c) {
    vec2 z = vec2(0.0);
    int iterations = 0;
    const int max_iterations = 1000;
    const float threshold = 4.0;
    while (iterations < max_iterations && dot(z, z) < threshold) {
        z = vec2(
            z.x * z.x - z.y * z.y + c.x,
            2.0 * z.x * z.y + c.y
        );
        iterations++;
    }
    return iterations;
}

void main() {
    vec2 frag_position = -1.0 + 2.0 * gl_FragCoord.xy / resolution;

    // Apply kaleidoscopic wedge symmetry around screen center
    vec2 symmetric_pos = apply_kaleidoscope(frag_position, 45.0);

    // Define zoomed Mandelbrot space ranges
    vec2 x_range = vec2(mandelbrot_center_x - 1.0, mandelbrot_center_x + 1.0);
    vec2 y_range = vec2(mandelbrot_center_y - 1.0, mandelbrot_center_y + 1.0);

    // Map symmetric screen position to Mandelbrot coordinates
    vec2 mandelbrot_pos = remap(symmetric_pos, zoom_factor, x_range, y_range);

    // Compute Mandelbrot iterations
    int iters = mandelbrot(mandelbrot_pos);

    // Color interpolation with block size 20 for richer colors
    float block_size = 10.0;
    float t = mod(float(iters), block_size) / block_size;
    vec3 color = mix(vec3(0.2, 0.0, 0.4), vec3(1.0, 0.9, 0.1), pow(t, 0.8));

    fragColor = vec4(color, 1.0);
}
