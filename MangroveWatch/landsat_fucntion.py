import os
import numpy as np
import pystac_client
import planetary_computer
import odc.stac
import matplotlib.pyplot as plt

# Source: https://planetarycomputer.microsoft.com/docs/quickstarts/reading-stac
def search_landsat_scenes(years, bbox, max_cloud=40):
    """Search the STAC catalog and return valid scenes per year."""
    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace,
    )

    # Searching the STAC catalog for Landsat scenes
    selected_items = {}
    for year in years:
        time_range = f"{year}-01-01/{year}-03-31"
        platform = "landsat-5" if year < 2013 else "landsat-8"

        search = catalog.search(
            collections=["landsat-c2-l2"],
            bbox=bbox,
            datetime=time_range,
            query={
                "platform": {"eq": platform},
                "eo:cloud_cover": {"lt": max_cloud}
            },
        )
        items = search.get_all_items()
        print(f"Year {year}: Found {len(items)} scenes with <{max_cloud}% cloud cover.")
        selected_items[year] = list(items)

    return selected_items


# Source: https://www.usgs.gov/faqs/how-do-i-use-a-scale-factor-landsat-level-2-science-products
def scale_landsat_sr(ds):
    """Scale Landsat Collection 2 Level-2 Surface Reflectance to 0-1 values."""
    scaled = ds * 0.0000275 - 0.2
    return scaled.clip(0, 1)


# Source: https://medium.com/@geonextgis/getting-started-with-microsoft-planetary-computer-stac-api-67cbebe96e5e
def plot_true_color(selected_items, bbox, output_dir="landsat_data"):
    """Render and save a natural colour composite for each year's selected scenes."""

    # Create an output folder
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    for year, items in selected_items.items():
        if not items:
            print(f"No items found for year {year}")
            continue

        data = odc.stac.stac_load(
            items,
            bands=["red", "green", "blue"],
            bbox=bbox,
            crs="EPSG:32649",  # UTM Zone 49N for Hainan Island
            resolution=100,
            groupby="solar_day",
        )

        # Mask true nodata 
        data = data.where(data > 0)

        data_scaled = scale_landsat_sr(data)

        # Median composite along time dimension
        composite = data_scaled.median(dim="time", skipna=True)

        # Natural colour composite
        rgb_data_array = composite[["red", "green", "blue"]].to_array(dim="band")
        fig, ax = plt.subplots(figsize=(10, 10))
        rgb_data_array.plot.imshow(robust=True, ax=ax)
        ax.set_title(f"Natural Color, Hainan Island, January {year}")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"hainan_rgb_{year}.png"))
        plt.show()
        plt.close(fig)


# Source: https://medium.com/@geonextgis/getting-started-with-microsoft-planetary-computer-stac-api-67cbebe96e5e
def plot_ndvi_ndwi(selected_items, bbox, output_dir="landsat_data"):
    """Compute and save NDVI/NDWI for each year's selected scenes."""

    # Create an output folder
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    ndvi_ndwi_results = {}

    for year, items in selected_items.items():
        if not items:
            continue

        # Load the bands needed for NDVI and NDWI
        data = odc.stac.stac_load(
            items,
            bands=["nir08", "red", "green"],
            bbox=bbox,
            crs="EPSG:32649",  # UTM Zone 49N for Hainan
            resolution=100,
            groupby="solar_day",
        )

        # Mask true nodata
        data = data.where(data > 0)

        data_scaled = scale_landsat_sr(data)
        composite = data_scaled.median(dim="time", skipna=True)

        # Convert to float so the negative values aren't lost
        green = composite["green"]
        red = composite["red"]
        nir = composite["nir08"]

        # Calculating the NDVI and NDWI
        ndvi = (nir - red) / (nir + red)
        ndwi = (green - nir) / (green + nir)
        ndvi_ndwi_results[year] = {"ndvi": ndvi, "ndwi": ndwi}

        # Plot the NDVI and NDWI side by side
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 9))
        ndvi.plot.imshow(
            ax=axes[0], vmin=-0.2, vmax=0.8, cmap="RdYlGn",
            cbar_kwargs={"aspect": 30, "pad": 0.03, "label": "NDVI"}
        )
        axes[0].set_title(f"NDVI, Hainan Island, January {year}")

        ndwi.plot.imshow(
            ax=axes[1], vmin=-0.5, vmax=0.5, cmap="YlGnBu",
            cbar_kwargs={"aspect": 30, "pad": 0.03, "label": "NDWI"}
        )
        axes[1].set_title(f"NDWI, Hainan Island, January {year}")

        # Save to disk
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"hainan_ndvi_ndwi_{year}.png"))
        plt.show()
        plt.close(fig)

    return ndvi_ndwi_results


# Calling the fucntions year by year (because otherwise you run out of memory)
years = [1996]
bbox = [108.506470, 18.151072, 111.088257, 20.190035]

# Search for scenes and pick the least cloudy one
selected_items = search_landsat_scenes(years, bbox, max_cloud=50)

# Generate the true colour image
plot_true_color(selected_items, bbox, output_dir="landsat_data")

# Generate the NDVI/NDWI image
ndvi_ndwi_results = plot_ndvi_ndwi(selected_items, bbox, output_dir="landsat_data")