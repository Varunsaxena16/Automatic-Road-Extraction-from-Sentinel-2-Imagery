"""
Post-processing module for road mask refinement.

Implements:
- Skeletonization (centerline extraction)
- Length-based component filtering
"""

import cv2
import numpy as np
from skimage.morphology import skeletonize


def extract_skeleton(binary_mask):
    skeleton = skeletonize(binary_mask > 0).astype(np.uint8)
    return skeleton


def filter_skeleton_by_length(skeleton, min_length=40):
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        skeleton, connectivity=8
    )
    filtered_skeleton = np.zeros_like(skeleton)
    for i in range(1, num_labels):
        length = stats[i, cv2.CC_STAT_AREA]
        if length >= min_length:
            filtered_skeleton[labels == i] = 1
    return filtered_skeleton

def refine_centerlines(binary_mask, min_length=40):
    skeleton = extract_skeleton(binary_mask)
    filtered = filter_skeleton_by_length(skeleton, min_length)
    return filtered
