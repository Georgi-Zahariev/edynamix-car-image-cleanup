# python3 -m venv car-cleanup-env
# source car-cleanup-env/bin/activate
# pip install --upgrade pip

# pip install -r requirements.txt

import os
import io
from PIL import Image
import numpy as np
from rembg import remove
from src.refine_edges import refine_edges_and_recover_parts

DATA_DIR = "data"
OUTPUT_DIR = "outputs"
ALLOWED_EXT = (".jpg", ".jpeg", ".png")

def remove_background_bytes(image_path):
    with open(image_path, "rb") as inp_file:
        input_data = inp_file.read()
    result = remove(input_data)
    return result

def process_image(image_path, output_path):
    print(f"Processing: {image_path}")

    # Step 1: Remove background
    removed_bytes = remove_background_bytes(image_path)
    rgba_img = Image.open(io.BytesIO(removed_bytes)).convert("RGBA")
    rgba_np = np.array(rgba_img)

    # Step 2: Refine edges and recover missing parts
    refined_np = refine_edges_and_recover_parts(rgba_np)

    # Step 3: Save
    Image.fromarray(refined_np).save(output_path)
    print(f"Saved: {output_path}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in os.listdir(DATA_DIR):
        if filename.lower().endswith(ALLOWED_EXT):
            input_path = os.path.join(DATA_DIR, filename)

            name, _ = os.path.splitext(filename)
            output_path = os.path.join(OUTPUT_DIR, f"{name}_cleaned.png")

            process_image(input_path, output_path)

if __name__ == "__main__":
    main()
