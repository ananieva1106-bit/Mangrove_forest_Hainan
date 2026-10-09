import os
import numpy as np
import pystac_client
import planetary_computer
import odc.stac
import rasterio
from scipy.ndimage import maximum_filter
from collections import defaultdict

# Start function here
def landsat_download(year,bbox, bands, crs, output_dir, n_scenes):
    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace,
    )

    items = list(catalog.search(
        collections=["landsat-c2-l2"],
        bbox=bbox,
        datetime=f"{year-1}-12-01/{year}-03-30",
        query={"platform": {"eq": "landsat-5" if year < 2013 else "landsat-8"}},
    ).items())

    # Keep the n least cloudy scenes per path/row tile
    tiles = defaultdict(list)
    for it in items:
        tiles[(it.properties["landsat:wrs_path"], it.properties["landsat:wrs_row"])].append(it)
    items = [
        it for tile in tiles.values()
        for it in sorted(tile, key=lambda i: i.properties["eo:cloud_cover"])[:n_scenes]
    ]
    print(f"{year}: {len(items)} scenes from {len(tiles)} tiles")

    ds = odc.stac.stac_load(
        items, bands=bands + ["qa_pixel"], bbox=bbox,
        crs=crs, resolution=100, groupby="solar_day",
    )

    # Cloud mask, grown by 1 pixel in y and x
    bad = maximum_filter(((ds["qa_pixel"].values & 0b11011) != 0).astype("uint8"),
                         size=(1, 3, 3)) > 0

    # Median composite -> (band, y, x)
    layers = []
    for b in bands:
        a = ds[b].values.astype("float32")
        a[bad | (a < 7273) | (a > 43636)] = np.nan
        a = (a * 0.0000275) - 0.2 # Convert raw DS to reflectance values (Source: https://www.usgs.gov/landsat-missions/landsat-collection-2-surface-reflectance)
        layers.append(np.nanmedian(a, axis=0))
    arr = np.stack(layers).astype("float32")

    # Create metadata profile
    profile = {
        "driver": "GTiff",
        "dtype": "float32",
        "nodata": np.nan,
        "crs": crs,
        "transform": ds.odc.geobox.affine,
        "count": arr.shape[0],
        "height": arr.shape[1],
        "width": arr.shape[2],
    }
    
    # Write file
    with rasterio.open(f"{output_dir}/{year}.tif", "w", **profile) as dst:
        dst.write(arr)
        dst.descriptions = bands