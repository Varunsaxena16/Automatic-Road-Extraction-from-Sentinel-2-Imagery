"""
Classical Road Segmentation Module.

Implements:
- Grayscale conversion
- Histogram equalization
- Canny edge detection
- Morphological refinement
- Small component removal
"""

import cv2
import numpy as np


def prepare_rgb(image):
    rgb = (image[:, :, :3] * 255).clip(0, 255).astype(np.uint8)
    return rgb


def enhance_contrast(rgb):
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    gray = cv2.equalizeHist(gray)
    return gray


def detect_edges(gray, threshold1=50, threshold2=150):
    edges = cv2.Canny(gray, threshold1, threshold2)
    return edges


def morphological_refinement(edges, kernel_size=3):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    mask = cv2.dilate(edges, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    binary_mask = (mask > 0).astype(np.uint8)
    return binary_mask


def remove_border_artifacts(binary_mask, border_size=15):
    mask = binary_mask.copy()
    mask[:border_size, :] = 0
    mask[-border_size:, :] = 0
    mask[:, :border_size] = 0
    mask[:, -border_size:] = 0
    return mask


def remove_small_components(binary_mask, min_area=150):
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        binary_mask, connectivity=8
    )
    clean_mask = np.zeros_like(binary_mask)
    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            clean_mask[labels == i] = 1
    return clean_mask


def classical_road_segmentation(image):
    rgb = prepare_rgb(image)
    gray = enhance_contrast(rgb)
    edges = detect_edges(gray)
    binary_mask = morphological_refinement(edges)
    binary_mask = remove_border_artifacts(binary_mask)
    clean_mask = remove_small_components(binary_mask)
    return clean_mask
