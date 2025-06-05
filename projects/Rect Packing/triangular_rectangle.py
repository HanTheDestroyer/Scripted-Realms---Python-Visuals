import numpy as np
from canvas import Canvas


class TriangularRectangle:
    """This class creates a rectangle using four triangles."""
    def __init__(self, a, b, c, d, base_color, canvas: Canvas):
        self.canvas = canvas
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.base_color = base_color
        # Calculate colors:
        multipliers = [1.0, 0.85, 0.7, 0.55]
        colors = []
        for m in multipliers:
            rgb = np.clip(self.base_color[:3] * m, 0, 255).astype(np.uint8)
            rgba = np.append(rgb, 255)
            colors.append(rgba)

        # Calculate the bounding box of the shape.
        x_min = min(a[0], b[0], c[0], d[0])
        x_max = max(a[0], b[0], c[0], d[0])
        y_min = min(a[1], b[1], c[1], d[1])
        y_max = max(a[1], b[1], c[1], d[1])
        self.x_range = np.array([x_min, x_max])
        self.y_range = np.array([y_min, y_max])
        # Calculate the center of the shape.
        center_ab = (a + b) / 2
        center_bc = (b + c) / 2
        center_cd = (c + d) / 2
        center_da = (d + a) / 2
        self.e = (center_ab + center_bc + center_cd + center_da) / 4
        # Calculate the max thickness for each line segment so that they can be turned into triangles.
        # BOTTOM TRIANGLE
        ab = self.b - self.a
        ae = self.e - self.a
        signed_thickness_aeb = self.scalar_cross(ab, ae) / np.linalg.norm(ab)
        # RIGHT TRIANGLE
        bc = self.c - self.b
        be = self.e - self.b
        signed_thickness_bec = self.scalar_cross(bc, be) / np.linalg.norm(bc)
        # TOP TRIANGLE
        cd = self.d - self.c
        ce = self.e - self.c
        signed_thickness_ced = self.scalar_cross(cd, ce) / np.linalg.norm(cd)
        # LEFT TRIANGLE
        da = self.a - self.d
        de = self.e - self.d
        signed_thickness_dea = self.scalar_cross(da, de) / np.linalg.norm(da)    
        # Draw the triangles on the canvas.
        self.draw_triangle(self.a, self.b, signed_thickness_aeb, colors[0]) 
        self.draw_triangle(self.b, self.c, signed_thickness_bec, colors[1])
        self.draw_triangle(self.c, self.d, signed_thickness_ced, colors[2])
        self.draw_triangle(self.d, self.a, signed_thickness_dea, colors[3])  

    @staticmethod
    def scalar_cross(a, b):
        """Returns the scalar cross product of two 2D vectors."""
        return a[0] * b[1] - a[1] * b[0]

    def draw_triangle(self, p1, p2, signed_thickness, color):
        """Draws a triangle on the canvas."""
        distance_range = np.array([0, signed_thickness]) if signed_thickness > 0 else np.array([signed_thickness, 0])
        for y in range(self.y_range[0], self.y_range[1]):
            for x in range(self.x_range[0], self.x_range[1]):
                fp = np.array([x, y])
                p1p2 = p2 - p1
                p1fp = fp - p1
                # Use scalar 2D cross product
                signed_distance = self.scalar_cross(p1p2, p1fp) / np.linalg.norm(p1p2)
                # Add projection constraint to clip band to triangle
                t = np.dot(p1p2, p1fp) / np.dot(p1p2, p1p2)
                taper = 1 - abs(0.5 - t) * 2  # Tapering factor
                if taper <= 0:
                    continue
                normalized_signed_distance = distance_range * taper
                epsilon = 0.5
                if normalized_signed_distance[0] - epsilon <= signed_distance <= normalized_signed_distance[1] + epsilon:
                    self.canvas.grid[y, x] = color



if __name__ == "__main__":
    canvas = Canvas(500, 500)
    a = np.array([10, 10])
    b = np.array([15, 10])
    c = np.array([15, 15])
    d = np.array([10, 15])
    color = np.array([200, 100, 50, 255], dtype=np.uint8)
    tri_rect = TriangularRectangle(a, b, c, d, color, canvas)
    print(f"Center of the rectangle: {tri_rect.e}")
    # Flip canvas.
    canvas.grid = np.flipud(canvas.grid)
    canvas.save_image("triangular_rectangle.png")
