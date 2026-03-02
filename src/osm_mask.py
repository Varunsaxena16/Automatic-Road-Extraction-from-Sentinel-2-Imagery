"""
OSM Road Mask Generation Module.

This module:
- Fetches OpenStreetMap roads for a given AOI
- Converts them to target CRS
- Rasterizes them into a binary mask
"""

import osmnx as ox
import geopandas as gpd
import numpy as np
from shapely.geometry import box
from rasterio.features import rasterize


def create_aoi_polygon(bounds, crs):
    aoi_polygon = box(bounds.left, bounds.bottom, bounds.right, bounds.top)
    aoi_gdf = gpd.GeoDataFrame(geometry=[aoi_polygon], crs=crs)
    aoi_gdf = aoi_gdf.to_crs(epsg=4326)

    return aoi_gdf.geometry.iloc[0]


def fetch_osm_roads(aoi_polygon_latlon):
    graph = ox.graph_from_polygon(
        aoi_polygon_latlon,
        network_type="drive"
    )

    roads_gdf = ox.graph_to_gdfs(graph, nodes=False)

    return roads_gdf


def rasterize_roads(roads_gdf, transform, crs, height, width):
    roads_gdf = roads_gdf.to_crs(crs)

    road_mask = rasterize(
        [(geom, 1) for geom in roads_gdf.geometry],
        out_shape=(height, width),
        transform=transform,
        fill=0,
        dtype=np.uint8
    )

    return road_mask
