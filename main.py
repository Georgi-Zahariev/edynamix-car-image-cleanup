# python3 -m venv car-cleanup-env
# source car-cleanup-env/bin/activate
# pip install --upgrade pip

# pip install -r requirements.txt


from PIL import Image            # Pillow: For image reading (not directly used here yet)
import numpy as np               # NumPy: Used in other image processing tasks
from rembg import remove         # rembg provides a simple `remove()` function for background removal
import os
import io

def remove_background_simple(image_path, output_path):
    # Open the image in binary mode (rembg expects bytes, not a Pillow object)
    with open(image_path, "rb") as inp_file:
        input_data = inp_file.read()

    # Use rembg to remove background. It returns image bytes (still in PNG format with transparency)
    result = remove(input_data)

    # Save the resulting image bytes to the output path (with transparent background)
    with open(output_path, "wb") as out_file:
        out_file.write(result)


def remove_background_advanced(image_path, output_path):
    with open(image_path, "rb") as inp_file:
        input_data = inp_file.read()

    result = remove(input_data)

    # Convert result to an image with alpha channel
    img = Image.open(io.BytesIO(result)).convert("RGBA")

    # Convert to NumPy array to edit pixel values
    np_img = np.array(img)

    # Create a mask where the alpha channel is semi-transparent (e.g., windows, reflections)
    alpha = np_img[:, :, 3]
    semi_transparent_mask = (alpha > 20) & (alpha < 220)  # Tunable range

    # Darken semi-transparent areas (simulate dark glass or clean surface)
    np_img[semi_transparent_mask, :3] = (30, 30, 30)  # Dark gray color
    np_img[semi_transparent_mask, 3] = 255  # Make it fully opaque

    # Convert back to image
    clean_img = Image.fromarray(np_img)

    # Save result
    clean_img.save(output_path)
    print(f"Cleaned image saved at {output_path}")

# ...existing code...

MODE = "simple"  # Change to "advanced" to use the advanced method

if __name__ == "__main__":
    data_folder = "data"
    files = [f for f in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, f))]

    for filename in files:
        name, ext = os.path.splitext(filename)
        input_path = os.path.join(data_folder, filename)
        output_path = os.path.join(data_folder, f"{name}_removedbg{ext}")

        if MODE == "simple":
            remove_background_simple(input_path, output_path)
        elif MODE == "advanced":
            remove_background_advanced(input_path, output_path)
        else:
            raise ValueError("Unknown MODE. Use 'simple' or 'advanced'.")

        print(f"Processed: {filename} -> {name}_removedbg{ext}")

    print("All files processed and saved with _removedbg.")
# ...existing code...