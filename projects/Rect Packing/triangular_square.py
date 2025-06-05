import numpy as np
from canvas import Canvas


class TriangularSquare:
    """This class creates a square using four triangles."""
    def __init__(self, center, side_length, base_color, canvas: Canvas):
        self.canvas = canvas
        half_length = side_length // 2
        self.a = np.array([center[0] - half_length, center[1] - half_length])
        self.b = np.array([center[0] + half_length, center[1] - half_length])
        self.c = np.array([center[0] + half_length, center[1] + half_length])
        self.d = np.array([center[0] - half_length, center[1] + half_length])
        self.base_color = base_color
        # Calculate colors:
        multipliers = [1.0, 0.85, 0.7, 0.55]
        colors = []
        for m in multipliers:
            rgb = np.clip(self.base_color[:3] * m, 0, 255).astype(np.uint8)
            rgba = np.append(rgb, 255)
            colors.append(rgba)

        # Calculate the bounding box of the shape.
        x_min = min(self.a[0], self.b[0], self.c[0], self.d[0])
        x_max = max(self.a[0], self.b[0], self.c[0], self.d[0])
        y_min = min(self.a[1], self.b[1], self.c[1], self.d[1])
        y_max = max(self.a[1], self.b[1], self.c[1], self.d[1])
        self.x_range = np.array([x_min, x_max])
        self.y_range = np.array([y_min, y_max])
        # Calculate the center of the shape.
        center_ab = (self.a + self.b) / 2
        center_bc = (self.b + self.c) / 2
        center_cd = (self.c + self.d) / 2
        center_da = (self.d + self.a) / 2
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
    color = np.array([200, 100, 50, 255], dtype=np.uint8)
    tri_rect = TriangularSquare(np.array([250, 250]), 100, color, canvas)
    print(f"Center of the rectangle: {tri_rect.e}")
    # Flip canvas.
    canvas.grid = np.flipud(canvas.grid)
    canvas.save_image("triangular_square.png")
