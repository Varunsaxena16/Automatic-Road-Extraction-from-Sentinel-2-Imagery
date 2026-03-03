# Automatic Road Extraction from Sentinel-2 Imagery

This project implements an end-to-end pipeline for automatic road extraction from Sentinel-2 satellite imagery using classical image processing techniques and geospatial post-processing.
The workflow includes image preprocessing, edge-based road segmentation, centerline extraction, raster-to-vector conversion, and semantic enrichment using OpenStreetMap (OSM) data.
Area of Interest: New Delhi, India  
Dataset: Sentinel-2 Level-2A (10m resolution)  

---

## Methodology

### 1. Data Acquisition and Preprocessing

- Sentinel-2 GeoTIFF loaded using rasterio
- Conversion from (C, H, W) to (H, W, C)
- NaN and infinite values sanitized
- Global min–max normalization applied
- RGB bands used for segmentation
- CRS and geospatial metadata preserved (EPSG:32643)

---

### 2. Road Segmentation (Classical Approach)

The road extraction pipeline is based on deterministic image processing:

- RGB → Grayscale conversion
- Histogram equalization (contrast enhancement)
- Canny edge detection
- Morphological dilation and closing
- Connected component filtering (area thresholding)

This produces a cleaned binary road mask.

---

### 3. Centerline Extraction

- Skeletonization using `skimage.morphology`
- Length-based filtering of connected components
- Extraction of continuous road centerlines

---

### 4. Raster to Vector Conversion

- Contour extraction using `skimage.measure.find_contours`
- Conversion from pixel coordinates to projected map coordinates
- Creation of LineString geometries
- Export as GeoJSON

---

### 5. Road Naming (Spatial Join)

Final road naming was performed in QGIS:

- Extracted centerlines were spatially joined with OpenStreetMap road vectors
- Road names were transferred using intersection/nearest spatial matching
- Final output contains named road geometries

---

## Tools & Libraries

- rasterio
- numpy
- opencv-python
- scikit-image
- geopandas
- shapely
- osmnx
- QGIS (for spatial join and topology refinement)

---

## Limitations

- Classical edge detection is sensitive to shadows and urban clutter
- Performance may degrade in dense built-up areas
- No deep learning model used
- Naming accuracy depends on OSM completeness

---

## Hardware

Pipeline tested on standard CPU environment (Google Colab).

---

## Future Improvements

- Replace classical segmentation with U-Net or DeepLabV3+
- Incorporate multi-spectral bands (NIR)
- Implement automated topology correction
- Add quantitative metrics (IoU, Precision, Recall)
