"""
Preprocessing module for Sentinel-2 road extraction pipeline.

Handles:
- GeoTIFF loading
- NaN/Inf sanitization
- Min-max normalization
- Metadata preservation
"""

import rasterio
import numpy as np


def load_geotiff(tif_path):
    with rasterio.open(tif_path) as src:
        image = src.read(masked=True).filled(0)
        transform = src.transform
        crs = src.crs
        profile = src.profile

    # Convert from (C, H, W) to (H, W, C)
    image = np.transpose(image, (1, 2, 0))

    return image, transform, crs, profile


def sanitize_image(image):
    """
    Replace NaN and infinite values with zeros.
    """
    return np.nan_to_num(image, nan=0.0, posinf=0.0, neginf=0.0)


def minmax_normalize(image):
    """
    Apply safe min-max normalization.
    """
    min_val = image.min()
    max_val = image.max()

    if max_val > min_val:
        image = (image - min_val) / (max_val - min_val)
    else:
        raise ValueError("Image has no dynamic range.")

    return image
