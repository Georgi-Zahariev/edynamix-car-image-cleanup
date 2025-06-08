# python3 -m venv car-cleanup-env
# source car-cleanup-env/bin/activate
# pip install --upgrade pip

# pip install -r requirements.txt


from PIL import Image            # Pillow: For image reading (not directly used here yet)
import numpy as np               # NumPy: Used in other image processing tasks
from rembg import remove         # rembg provides a simple `remove()` function for background removal

def remove_background(image_path, output_path):
    # Open the image in binary mode (rembg expects bytes, not a Pillow object)
    with open(image_path, "rb") as inp_file:
        input_data = inp_file.read()

    # Use rembg to remove background. It returns image bytes (still in PNG format with transparency)
    result = remove(input_data)

    # Save the resulting image bytes to the output path (with transparent background)
    with open(output_path, "wb") as out_file:
        out_file.write(result)

# Entry point when running `python app.py`
if __name__ == "__main__":
    # You can change these paths for testing with different images
    remove_background("data/car1.jpg", "outputs/car1_cleaned.png")
    print("Background removed and saved.")
