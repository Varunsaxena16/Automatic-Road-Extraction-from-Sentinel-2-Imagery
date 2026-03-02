"""
Vectorization module.

Converts binary centerline raster into geospatial LineString vectors
and exports as GeoJSON.
"""

import numpy as np
import geopandas as gpd
from shapely.geometry import LineString
from skimage.measure import find_contours
from rasterio.transform import xy


def contours_to_lines(binary_mask, min_points=20):
    contours = find_contours(binary_mask, level=0.5)
    lines = []
    for contour in contours:
        if len(contour) < min_points:
            continue
        coords = [(c[1], c[0]) for c in contour]
        lines.append(LineString(coords))
    return lines

def pixel_to_map_coords(lines, transform):
    def convert_line(line):
        return LineString([
            xy(transform, int(y), int(x))
            for x, y in line.coords
        ])
    return [convert_line(line) for line in lines]

def create_geodataframe(lines, crs):
    return gpd.GeoDataFrame(geometry=lines, crs=crs)


def vectorize_centerlines(binary_mask, transform, crs, min_points=20):
    binary = (binary_mask > 0).astype(np.uint8)
    lines_pixel = contours_to_lines(binary, min_points)
    lines_map = pixel_to_map_coords(lines_pixel, transform)
    gdf = create_geodataframe(lines_map, crs)
    return gdf

def export_geojson(gdf, output_path):
    gdf.to_file(output_path, driver="GeoJSON")
