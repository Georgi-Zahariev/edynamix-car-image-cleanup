import cv2
import numpy as np
from PIL import Image


def refine_edges_and_recover_parts(rgba_np, dilate_radius=5):
    h, w = rgba_np.shape[:2]
    alpha = rgba_np[:, :, 3]
    confident_mask = (alpha > 128).astype(np.uint8) * 255
    closed_mask = cv2.morphologyEx(confident_mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    dilated_mask = cv2.dilate(closed_mask, np.ones((dilate_radius, dilate_radius), np.uint8), iterations=1)
    blended_mask = cv2.bitwise_or(confident_mask, dilated_mask)
    rgb = rgba_np[:, :, :3]
    black_pixel_mask = (rgb[:, :, 0] < 15) & (rgb[:, :, 1] < 15) & (rgb[:, :, 2] < 15)
    black_pixel_mask = black_pixel_mask.astype(np.uint8) * 255
    cleanup_mask = cv2.bitwise_not(black_pixel_mask)
    final_mask = cv2.bitwise_and(blended_mask, cleanup_mask)
    refined_rgba = np.zeros_like(rgba_np)
    for c in range(3):
        refined_rgba[:, :, c] = np.where(final_mask == 255, rgba_np[:, :, c], 0)
    refined_rgba[:, :, 3] = final_mask
    return refined_rgba


"""
def refine_edges_and_recover_parts(rgba_np, dilate_radius=5):
    h, w = rgba_np.shape[:2]
    alpha = rgba_np[:, :, 3]
    binary_mask = (alpha > 128).astype(np.uint8) * 255
    closed_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    dilated_mask = cv2.dilate(closed_mask, np.ones((dilate_radius, dilate_radius), np.uint8), iterations=1)
    contours, _ = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask_hull = np.zeros((h, w), dtype=np.uint8)
    for cnt in contours:
        hull = cv2.convexHull(cnt)
        cv2.drawContours(mask_hull, [hull], -1, 255, thickness=-1)
    final_mask = cv2.bitwise_or(dilated_mask, mask_hull)
    refined_rgba = rgba_np.copy()
    for c in range(3):
        refined_rgba[:, :, c] = np.where(final_mask == 255, rgba_np[:, :, c], 0)
    refined_rgba[:, :, 3] = final_mask
    return refined_rgba

"""

""" def refine_edges_and_recover_parts(rgba_np, radius=3):
    
    #Smooths alpha edges.
    #Fills missing small parts (shadows, wheels, bumpers).
    
    # Extract alpha and binary mask of the car
    alpha = rgba_np[:, :, 3]
    car_mask = (alpha > 128).astype(np.uint8) * 255

    # --- Step 1: Smooth edges ---
    blurred_alpha = cv2.GaussianBlur(alpha, (radius * 2 + 1, radius * 2 + 1), 0)

    # --- Step 2: Morphological closing to reconnect broken parts ---
    kernel = np.ones((5, 5), np.uint8)
    closed_mask = cv2.morphologyEx(car_mask, cv2.MORPH_CLOSE, kernel)

    # --- Step 3: Fill small holes inside car mask ---
    filled_mask = cv2.morphologyEx(closed_mask, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))

    # --- Step 4: Dilate slightly to recover extra lost edges (optional) ---
    dilated_mask = cv2.dilate(filled_mask, kernel, iterations=1)

    # --- Step 5: Combine with original RGB ---
    refined_rgba = rgba_np.copy()
    refined_rgba[:, :, 3] = cv2.normalize(blurred_alpha, None, 0, 255, cv2.NORM_MINMAX)

    # Apply corrected mask: keep RGB only where mask is valid
    refined_rgba[dilated_mask == 0] = [0, 0, 0, 0]

    return refined_rgba
"""