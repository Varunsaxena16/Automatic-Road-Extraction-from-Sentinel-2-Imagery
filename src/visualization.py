"""
Visualization utilities for road extraction validation.
"""

import matplotlib.pyplot as plt


def overlay_osm_vs_extracted(rgb_image, osm_mask, extracted_mask):
    plt.figure(figsize=(12, 6))

    # RGB + OSM
    plt.subplot(1, 2, 1)
    plt.imshow(rgb_image[:, :, :3])
    plt.imshow(osm_mask, cmap="Reds", alpha=0.6)
    plt.title("RGB + OSM Roads")
    plt.axis("off")

    # RGB + Extracted
    plt.subplot(1, 2, 2)
    plt.imshow(rgb_image[:, :, :3])
    plt.imshow(extracted_mask, cmap="Greens", alpha=0.9)
    plt.title("RGB + Extracted Road Centerlines")
    plt.axis("off")

    plt.tight_layout()
    plt.show()
