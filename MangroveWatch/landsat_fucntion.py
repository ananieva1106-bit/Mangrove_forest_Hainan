import os
import pystac_client
import planetary_computer
import odc.stac
import matplotlib.pyplot as plt

# Source: https://planetarycomputer.microsoft.com/docs/quickstarts/reading-stac
def search_landsat_scenes(years, bbox):
    """Search the STAC catalog and return the least-cloudy scene per year."""
    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace,
    )

    # Searching the STAC catalog for Landsat scenes
    all_items = {}
    for year in years:
        time_range = f"{year}-01-01/{year}-01-31"
        platform = "landsat-5" if year < 2013 else "landsat-8"

        search = catalog.search(
            collections=["landsat-c2-l2"],
            bbox=bbox,
            datetime=time_range,
            query={"platform": {"eq": platform}},
        )
        items = search.get_all_items()
        print(year, len(items))
        all_items[year] = items

    # Pick the least cloudy scenes per year
    selected_items = {}
    for year, items in all_items.items():
        best_per_tile = {}
        for item in items:
            tile = (item.properties["landsat:wrs_path"], item.properties["landsat:wrs_row"])
            cloud = item.properties["eo:cloud_cover"]
            if tile not in best_per_tile or cloud < best_per_tile[tile].properties["eo:cloud_cover"]:
                best_per_tile[tile] = item
        selected_items[year] = list(best_per_tile.values())

    return all_items, selected_items


# Source: https://medium.com/@geonextgis/getting-started-with-microsoft-planetary-computer-stac-api-67cbebe96e5e
def plot_true_color(selected_items, bbox, output_dir="landsat_data"):
    """Render and save a natural colour composite for each year's selected scenes."""

    # Create an output folder
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for year, items in selected_items.items():
        data = odc.stac.stac_load(
            items, bands=["red", "green", "blue"], bbox=bbox,
            crs="utm", resolution=100, groupby="solar_day"
        )
        composite = data.median(dim="time")

        # Natural colour composite
        rgb_data_array = composite[["red", "green", "blue"]].to_array()
        fig, ax = plt.subplots(figsize=(10, 10))
        rgb_data_array.plot.imshow(robust=True, ax=ax)
        ax.set_title(f"Natural Color, Hainan Island, January {year}")
        plt.savefig(os.path.join(output_dir, f"hainan_rgb_{year}.png"))
        plt.show()
        plt.close(fig)


# Source: https://medium.com/@geonextgis/getting-started-with-microsoft-planetary-computer-stac-api-67cbebe96e5e
def plot_ndvi_ndwi(selected_items, bbox, output_dir="landsat_data"):
    """Compute and save NDVI/NDWI for each year's selected scenes."""

    # Create an output folder
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    ndvi_ndwi_results = {}

    for year, items in selected_items.items():

        # Load the bands needed for NDVI and NDWI
        data = odc.stac.stac_load(
            items, bands=["nir08", "red", "green"], bbox=bbox,
            crs="utm", resolution=100, groupby="solar_day"
        )
        composite = data.median(dim="time")

        # Convert to float so the negative values aren't lost
        green = composite["green"].astype("float")
        red = composite["red"].astype("float")
        nir = composite["nir08"].astype("float")

        # Calculating the NDVI and NDWI
        ndvi = (nir - red) / (nir + red)
        ndwi = (green - nir) / (green + nir)
        ndvi_ndwi_results[year] = {"ndvi": ndvi, "ndwi": ndwi}

        # Plot the NDVI and NDWI side by side
        fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(28, 12))
        ndvi.plot.imshow(ax=axes[0], robust=True, cmap="RdYlGn", add_colorbar=True,
                          cbar_kwargs={"aspect": 30, "pad": 0.03, "label": "NDVI"})
        axes[0].set_title(f"NDVI, Hainan Island, January {year}")

        ndwi.plot.imshow(ax=axes[1], robust=True, cmap="YlGnBu", add_colorbar=True,
                          cbar_kwargs={"aspect": 30, "pad": 0.03, "label": "NDWI"})
        axes[1].set_title(f"NDWI, Hainan Island, January {year}")

        # Save to disk
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"hainan_ndvi_ndwi_{year}.png"))
        plt.show()
        plt.close(fig)

    return ndvi_ndwi_results


# Calling the fucntions year by year (because otherwise you run out of memory)
years = [1990]
bbox = [108.506470, 18.151072, 111.088257, 20.190035]

# Search for scenes and pick the least cloudy one
all_items, selected_items = search_landsat_scenes(years, bbox)

# Generate the true colour image
plot_true_color(selected_items, bbox, output_dir="landsat_data")

# Generate the NDVI/NDWI image
ndvi_ndwi_results = plot_ndvi_ndwi(selected_items, bbox, output_dir="landsat_data")