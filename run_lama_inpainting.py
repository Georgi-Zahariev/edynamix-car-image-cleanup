import cv2
import numpy as np
from iopaint.model_manager import ModelManager
from iopaint.schema import ApiConfig
from PIL import Image

def load_image(path):
    img = Image.open(path).convert("RGB")
    return np.array(img)

def generate_edge_mask(image_np, blur_radius=3, threshold=30):
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (blur_radius * 2 + 1, blur_radius * 2 + 1), 0)
    edges = cv2.Canny(blurred, threshold, threshold * 3)
    dilated = cv2.dilate(edges, np.ones((5, 5), np.uint8), iterations=1)
    return dilated
# ...existing code...

from iopaint.schema import ApiConfig, Device, InteractiveSegModel, RealESRGANModel

def run_lama_inpainting(image_path, output_path, model_name='cv2'):
    image_np = load_image(image_path)
    mask_np = generate_edge_mask(image_np)

    cv2.imwrite("outputs/debug_edge_mask.png", mask_np)

    config = ApiConfig(
        host="127.0.0.1",
        port=8080,
        inbrowser=False,
        model=model_name,
        no_half=True,
        low_mem=False,
        cpu_offload=False,
        disable_nsfw_checker=True,
        local_files_only=False,
        cpu_textencoder=False,
        device=Device.cpu,  # or Device.gpu if available
        input=None,         # or Path("outputs") if needed
        mask_dir=None,
        output_dir=None,
        quality=1,          # set to an int value as required
        enable_interactive_seg=False,
        interactive_seg_model=InteractiveSegModel.vit_b,  # <-- Use a valid value from your schema
        interactive_seg_device=Device.cpu,
        enable_remove_bg=False,
        remove_bg_device=Device.cpu,
        remove_bg_model="",
        enable_anime_seg=False,
        enable_realesrgan=False,
        realesrgan_device=Device.cpu,
        realesrgan_model=RealESRGANModel.RealESRGAN_x4plus,  # or another valid value
        enable_gfpgan=False,
        gfpgan_device=Device.cpu,
        enable_restoreformer=False,
        restoreformer_device=Device.cpu,
        enable_controlnet=False,
    )

    model = ModelManager(config.model, config.device)

    image_pil = Image.fromarray(image_np).convert("RGB")
    mask_pil = Image.fromarray(mask_np).convert("L")

    result = model(image_pil, mask_pil, config)
    result.save(output_path)
    print(f"✅ Inpainting complete. Saved to {output_path}")

# ...existing code... 

import os

if __name__ == "__main__":
    input_folder = "outputs"
    for filename in os.listdir(input_folder):
        if not filename.endswith(".png"):
            continue
        if "inpainted" in filename or "debug" in filename:
            continue

        input_path = os.path.join(input_folder, filename)
        name_wo_ext = os.path.splitext(filename)[0]
        output_path = os.path.join(input_folder, f"{name_wo_ext}_inpainted.png")

        print(f"🎯 Inpainting: {filename}")
        run_lama_inpainting(input_path, output_path)
