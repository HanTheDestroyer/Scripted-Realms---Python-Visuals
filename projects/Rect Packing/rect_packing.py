from canvas import Canvas
from triangular_square import TriangularSquare
import numpy as np
from PIL import Image

def pack_circles(canvas):
    num_squares = [10, 100, 300, 500, 10000]
    square_sizes = [200, 100, 50, 20, 10]

    for i in range(len(num_squares)):
        num = num_squares[i]
        size = square_sizes[i]
        max_attempts_per_square = 250
        counter = 0
        attempts = 0
        while counter < num and attempts < num * max_attempts_per_square:
            attempts += 1
            # Select a random position for the square.
            x = np.random.randint(size // 2, canvas.columns - size // 2)
            y = np.random.randint(size // 2, canvas.rows - size // 2)
            # Check if the square can be placed at the position (x, y).
            can_place = True
            x_min = x - size // 2
            x_max = x + size // 2
            y_min = y - size // 2
            y_max = y + size // 2
            if x_min < 0 or y_min < 0 or x_max > canvas.columns or y_max > canvas.rows:
                can_place = False
            else:
                canvas_part = canvas.grid[y_min:y_max, x_min:x_max]
                if np.any(canvas_part[..., 3] > 0):
                    can_place = False
            if can_place:
                color = np.random.randint(0, 255, size=4, dtype=np.uint8)
                color[3] = 255
                square = TriangularSquare(np.array([x, y]), size, color, canvas)
                counter += 1
            print(counter)

if __name__ == "__main__":
    canvas = Canvas(2000, 2000)
    pack_circles(canvas)
    # Flip canvas.
    canvas.grid = np.flipud(canvas.grid)
    canvas.save_image("triangular_square_packing.png")
    print("Packing completed and image saved as 'triangular_square_packing.png'.")

    # # Calculate the amount of packing percentage.
    # image = Image.open(r"C:/Users/han/Documents/Creative Coding/Outputs/triangular_square_packing.png")
    # image_np = np.array(image)
    # # Count non-transparent pixels (alpha == 255)
    # if image_np.shape[-1] == 4:
    #     packed_pixels = np.sum(image_np[..., 3] == 255)
    #     total_pixels = image_np.shape[0] * image_np.shape[1]
    #     packing_percentage = (packed_pixels / total_pixels) * 100
    #     print(f"Packing percentage: {packing_percentage:.2f}%")
    # else:
    #     print("Image does not have an alpha channel.")


