import os
import pystac_client
import planetary_computer
import odc.stac
import rioxarray

years = [1990]
bbox = [108.506470, 18.151072, 111.088257, 20.190035]
bands = ["red", "nir08", "swir16"]
output_dir = "data/landsat_data"
time_range_start = "12-01"
time_range_end = "03-30"
os.makedirs(output_dir, exist_ok=True)

catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)

for year in years:
    # Find all scenes from January to March
    search = catalog.search(
        collections=["landsat-c2-l2"],
        bbox=bbox,
        datetime=f"{year-1}-{time_range_start}/{year}-{time_range_end}",
        query={"platform": {"eq": "landsat-5" if year < 2013 else "landsat-8"}},
    )
    items = list(search.items())
    print(f"{year}: {len(items)} scenes")

    # Load them all
    data = odc.stac.stac_load(
        items,
        bands=bands + ["qa_pixel"], # For cloud masking
        bbox=bbox,
        crs="EPSG:32649",
        resolution=100,
        groupby="solar_day",
    )
    
    # # Cloud mask: True where the pixel is empty, cloud, cloud edge or cloud shadow
    # cloud = (data["qa_pixel"] & 0b11011) != 0

    # for band in bands:
    #     # Masked pixels become NaN, then average over time ignoring NaN
    #     composite = data[band].where(~cloud).mean(dim="time", skipna=True).astype("float32")
    #     composite.rio.write_nodata(float("nan")).rio.to_raster(f"{output_dir}/{band}_{year}.tif")
    #     print(f"Saved {band}_{year}.tif")

    # Mask: QA flags, slightly grown to catch cloud/shadow edges
    bad = (data["qa_pixel"] & 0b11011) != 0
    bad = bad.astype("uint8").rolling(x=3, y=3, center=True, min_periods=1).max() > 0

    for band in bands:
        # Also drop invalid reflectance values
        ok = (~bad) & (data[band] >= 7273) & (data[band] <= 43636)

        # Median is far less sensitive to leftover outliers than the mean
        composite = data[band].where(ok).median(dim="time", skipna=True).astype("float32")
        composite.rio.write_nodata(float("nan")).rio.to_raster(f"{output_dir}/{band}_{year}.tif")